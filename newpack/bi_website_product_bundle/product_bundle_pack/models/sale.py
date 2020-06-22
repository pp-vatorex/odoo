# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
##############################################################################


from odoo import api, models, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import SUPERUSER_ID



class SaleOrderLine(models.Model):
	_inherit = 'sale.order.line'

	@api.depends('move_ids.state', 'move_ids.scrapped', 'move_ids.product_uom_qty', 'move_ids.product_uom')
	def _compute_qty_delivered(self):
		super(SaleOrderLine, self)._compute_qty_delivered()
		for line in self:  # TODO: maybe one day, this should be done in SQL for performance sake
			if line.qty_delivered_method == 'stock_move':
				qty = 0.0
				flag = False
				if line.product_id.is_pack == True:
					list_of_sub_product = []
					for product_item in line.product_id.pack_ids:
						list_of_sub_product.append(product_item.product_id)
					for move in line.move_ids.filtered(lambda r: r.state == 'done' and not r.scrapped and  r.product_id in list_of_sub_product  ):
						if move.state == 'done' and move.product_uom_qty == move.quantity_done:
							flag = True
						else:
							flag = False
							break
					if flag == True:
						line.qty_delivered = line.product_uom_qty
					  
				else:
					outgoing_moves, incoming_moves = line._get_outgoing_incoming_moves()
					for move in outgoing_moves:
						if move.state != 'done':
							continue
						qty += move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom, rounding_method='HALF-UP')
					for move in incoming_moves:
						if move.state != 'done':
							continue
						qty -= move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom, rounding_method='HALF-UP')
					line.qty_delivered = qty


	@api.onchange('product_id', 'product_uom_qty')
	def _compute_qty_to_deliver(self):
		res = super(SaleOrderLine, self)._compute_qty_to_deliver()
		for i in self:
			if i.product_id.is_pack:
				if i.product_id.type == 'product':
					warning_mess = {}
					for pack_product in i.product_id.pack_ids:
						qty = i.product_uom_qty
						if qty * pack_product.qty_uom > pack_product.product_id.virtual_available:
							warning_mess = {
									'title': _('Not enough inventory!'),
									'message' : ('You plan to sell %s but you only have %s %s available, and the total quantity to sell is %s !' % (qty, pack_product.product_id.virtual_available, pack_product.product_id.name, qty * pack_product.qty_uom))
									}
							return {'warning': warning_mess}
			else:
				return res

	def _action_launch_stock_rule(self, previous_product_uom_qty=False):
		"""
		Launch procurement group run method with required/custom fields genrated by a
		sale order line. procurement group will launch '_run_pull', '_run_buy' or '_run_manufacture'
		depending on the sale order line product rule.
		"""
		precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
		procurements = []
		errors = []
		for line in self:
			if line.state != 'sale' or not line.product_id.type in ('consu','product'):
				continue
			qty = line._get_qty_procurement(previous_product_uom_qty)
			if float_compare(qty, line.product_uom_qty, precision_digits=precision) >= 0:
				continue

			group_id = line._get_procurement_group()
			if not group_id:
				group_id = self.env['procurement.group'].create(line._prepare_procurement_group_vals())
				line.order_id.procurement_group_id = group_id
			else:
				# In case the procurement group is already created and the order was
				# cancelled, we need to update certain values of the group.
				if line.product_id.pack_ids:
					values = line._prepare_procurement_values(group_id=line.order_id.procurement_group_id)
					for val in values:
						try:
							pro_id = self.env['product.product'].browse(val.get('product_id'))
							stock_id = self.env['stock.location'].browse(val.get('partner_dest_id'))
							product_uom_obj = self.env['uom.uom'].browse(val.get('product_uom'))
							procurements.append(self.env['procurement.group'].Procurement(
								pro_id, 0, product_uom_obj,
								line.order_id.partner_shipping_id.property_stock_customer,
								val.get('name'), val.get('origin'), line.order_id.company_id, val
							))
						except UserError as error:
							errors.append(error.name)
				else:
					updated_vals = {}
					if group_id.partner_id != line.order_id.partner_shipping_id:
						updated_vals.update({'partner_id': line.order_id.partner_shipping_id.id})
					if group_id.move_type != line.order_id.picking_policy:
						updated_vals.update({'move_type': line.order_id.picking_policy})
					if updated_vals:
						group_id.write(updated_vals)

			if line.product_id.pack_ids:
				values = line._prepare_procurement_values(group_id=line.order_id.procurement_group_id)
				# product_qty = line.product_uom_qty - qty
				for val in values:
					try:
						pro_id = self.env['product.product'].browse(val.get('product_id'))
						stock_id = self.env['stock.location'].browse(val.get('partner_dest_id'))
						product_uom_obj = self.env['uom.uom'].browse(val.get('product_uom'))
						procurements.append(self.env['procurement.group'].Procurement(
							pro_id, val.get('product_qty'), product_uom_obj,
							line.order_id.partner_shipping_id.property_stock_customer,
							val.get('name'), val.get('origin'), line.order_id.company_id, val
						))
					except UserError as error:
						errors.append(error.name)
			else:
				values = line._prepare_procurement_values(group_id=group_id)
				product_qty = line.product_uom_qty - qty

				line_uom = line.product_uom
				quant_uom = line.product_id.uom_id
				product_qty, procurement_uom = line_uom._adjust_uom_quantities(product_qty, quant_uom)
				procurements.append(self.env['procurement.group'].Procurement(
					line.product_id, product_qty, procurement_uom,
					line.order_id.partner_shipping_id.property_stock_customer,
					line.name, line.order_id.name, line.order_id.company_id, values))
		if procurements:
			self.env['procurement.group'].run(procurements)
		return True


	def _prepare_procurement_values(self, group_id):
		res = super(SaleOrderLine, self)._prepare_procurement_values(group_id=group_id)
		values = []
		date_planned = self.order_id.date_order\
			+ timedelta(days=self.customer_lead or 0.0) - timedelta(days=self.order_id.company_id.security_lead)
		if  self.product_id.pack_ids:
			for item in self.product_id.pack_ids:
				line_route_ids = self.env['stock.location.route'].browse(self.route_id.id)
				values.append({
					'name': item.product_id.name,
					'origin': self.order_id.name,
					'date_planned': date_planned,
					'product_id': item.product_id.id,
					'product_qty': item.qty_uom * abs(self.product_uom_qty),
					'product_uom': item.uom_id and item.uom_id.id,
					'company_id': self.order_id.company_id,
					'group_id': group_id,
					'sale_line_id': self.id,
					'warehouse_id' : self.order_id.warehouse_id and self.order_id.warehouse_id,
					'location_id': self.order_id.partner_shipping_id.property_stock_customer.id,
					'route_ids': self.route_id and line_route_ids or [],
					'partner_dest_id': self.order_id.partner_shipping_id,
					'partner_id': self.order_id.partner_shipping_id.id
				})
			return values
		else:
			res.update({
				'company_id': self.order_id.company_id,
				'group_id': group_id,
				'sale_line_id': self.id,
				'date_planned': date_planned,
				'route_ids': self.route_id,
				'warehouse_id': self.order_id.warehouse_id or False,
				'partner_dest_id': self.order_id.partner_shipping_id,
				'partner_id': self.order_id.partner_shipping_id.id,
				'company_id': self.order_id.company_id,
			})    
		return res
		

class ProcurementRule(models.Model):
	_inherit = 'stock.rule'
	
	def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):
		result = super(ProcurementRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, values, group_id)
		
		if  product_id.pack_ids:
			for item in product_id.pack_ids:
				result.update({
					'product_id': item.product_id.id,
					'product_uom': item.uom_id and item.uom_id.id,
					'product_uom_qty': item.qty_uom,
					'origin': origin,
					})
		return result

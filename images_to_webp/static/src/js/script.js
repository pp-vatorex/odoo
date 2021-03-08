odoo.define('images_to_webp.image_optimize_dialog', function (require) {
    var ImageOptimizeDialog = require('wysiwyg.widgets.image_optimize_dialog');
    var core = require('web.core');
    var _t = core._t;

    ImageOptimizeDialog.ImageOptimizeDialog.include({
        init: function (parent, params, options) {
            this._super.apply(this, arguments);

            this.isExisting = params.isExisting;
            this.attachment = params.attachment;
            // We do not support resizing and quality for:
            //  - SVG because it doesn't make sense
            //  - GIF because our current code is not made to handle all the frames
            this.disableResize = ['image/jpeg', 'image/jpe', 'image/jpg', 'image/png', 'image/webp'].indexOf(this.attachment.mimetype) === -1;
            this.disableQuality = this.disableResize;
            this.toggleQuality = this.attachment.mimetype === 'image/png';
            this.optimizedWidth = Math.min(params.optimizedWidth || this.attachment.image_width, this.attachment.image_width);
            this.defaultQuality = this.isExisting ? 100 : 80;
            this.defaultWidth = parseInt(this.isExisting ? this.attachment.image_width : this.optimizedWidth);
            this.defaultHeight = parseInt(this.isExisting || !this.attachment.image_width ? this.attachment.image_height :
                this.optimizedWidth / this.attachment.image_width * this.attachment.image_height);

            this.suggestedWidths = [];
            this._addSuggestedWidth(128, '128');
            this._addSuggestedWidth(256, '256');
            this._addSuggestedWidth(512, '512');
            this._addSuggestedWidth(1024, '1024');
            this._addSuggestedWidth(this.optimizedWidth,
                _.str.sprintf(_t("%d (Suggested)"), this.optimizedWidth));
            this.suggestedWidths.push({
                'width': this.attachment.image_width,
                'text': _.str.sprintf(_t("%d (Original)"), this.attachment.image_width),
            });
            this.suggestedWidths = _.sortBy(this.suggestedWidths, 'width');
            this._updatePreview = _.debounce(this._updatePreview.bind(this), 300);
        },
    });

    return {
        ImageOptimizeDialog: ImageOptimizeDialog,
    };
});

odoo.define('images_to_webp.media', function (require) {
    var FileWidgetClass = require('wysiwyg.widgets.media');


    FileWidgetClass.FileWidget.include({
        IMAGE_MIMETYPES: ['image/gif', 'image/jpe', 'image/jpeg', 'image/jpg', 'image/gif', 'image/png', 'image/svg+xml', 'image/webp'],
    });

    return FileWidgetClass;
});

odoo.define('images_to_webp.editor', function (require) {

    var EditorMenuBar = require('web_editor.editor');

    EditorMenuBar.Class.include({
        init: function (parent, options) {
            var self = this;
            var res = this._super.apply(this, arguments);

            $('body picture').each(function (_, elem) {
                $(elem).replaceWith($(elem).find('img'));
            });

            return res;
        }
    });

    return {
        Class: EditorMenuBar,
    };

});
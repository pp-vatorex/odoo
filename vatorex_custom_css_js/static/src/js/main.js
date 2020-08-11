$(document).ready(function() {
    // Display Alt-Tag in images in Blog
    var blog = $( "body" ).not(".editor_enable").find($("#o_wblog_post_content"));
    blog.find('img').each(function() {
        var data_vatorex_caption = this.data("vatorex_caption")
        if(!data_caption) {
            var alt = this.alt;
            //this.data("vatorex_caption", alt);
            //$(this).after('<div class="figure-caption">'+ alt + '</div>');
        }
    });

    // Additional jQuery here
    console.log('custom js is ready');
});

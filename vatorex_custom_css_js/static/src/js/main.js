$(document).ready(function() {
    // Display Alt-Tag in images in Blog
    var blog = $( "body" ).not(".editor_enable").find($("#o_wblog_post_content"));
    blog.find('img').each(function() {
        var data_caption = this.attr("data-caption")
        if(!data_caption) {
            var alt = this.alt;
            this.data("caption", alt);
            $(this).after('<div class="figure-caption">'+ alt + '</div>');
        }
    });

    // Additional jQuery here
    console.log('custom js is ready');
});

$(document).ready(function() {
    // Display Alt-Tag in images in Blog
    $("#o_wblog_post_content").find('img').each(function() {
         var alt = this.alt;
        $(this).after('<div class="figure-caption">'+ alt + '</div>');
    });

    // Additional jQuery here
    console.log('custom js is ready');
});

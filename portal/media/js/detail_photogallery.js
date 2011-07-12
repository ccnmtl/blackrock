function detailcarousel_initCallback(carousel) {
    // Link selectors
    jQuery(".jcarousel-selector").bind('click', function() {
        var idx = parseInt(jQuery(this).children("input.idx").val(), 10);
        carousel.scroll(idx, false);
    });
}

function detailcarousel_visibleOutCallback(carousel, item, pos, action) {
    
}

function detailcarousel_visibleInCallback(carousel, item, pos, action) {
    jQuery(".jcarousel-selected").removeClass("jcarousel-selected");
    var id = jQuery(item).children('input.selector').val();
    jQuery("#"+id).addClass("jcarousel-selected");
    
    jQuery(".jcarousel-caption").hide();
    var id = jQuery(item).children('input.caption').val();
    jQuery("#"+id).show();
}

jQuery(document).ready(function() {
    jQuery('#scrolling-photo-gallery').jcarousel({
        wrap: "circular",
        scroll: 1,
        initCallback: detailcarousel_initCallback,
        itemVisibleOutCallback: detailcarousel_visibleOutCallback,
        itemVisibleInCallback: { onBeforeAnimation: detailcarousel_visibleInCallback, onAfterAnimation: null }
     });
    
    if (!document.getElementById("related-items")) {
        var map = jQuery("#map_canvas");
        var maxHeight = map.css("max-height")
        var leftHeight = jQuery("#left").innerHeight();

        if (leftHeight > maxHeight) {
            jQuery(map).css("height", maxHeight);
        } else {
            jQuery(map).css("height", leftHeight);
        }
    }
});

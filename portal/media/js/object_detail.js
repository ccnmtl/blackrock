function detailcarousel_initCallback(carousel) {
    // Link selectors
    jQuery(".jcarousel-selector").bind('click', function () {
        var idx = parseInt(jQuery(this).children("input.idx").val(), 10);
        carousel.scroll(idx, false);
    });
}

function detailcarousel_visibleOutCallback(carousel, item, pos, action) {
    
}

function detailcarousel_visibleInCallback(carousel, item, pos, action) {
    jQuery(".jcarousel-selected").removeClass("jcarousel-selected");
    var id = jQuery(item).children('input.selector').val();
    jQuery("#" + id).addClass("jcarousel-selected");
    
    jQuery(".jcarousel-caption").hide();
    id = jQuery(item).children('input.caption').val();
    jQuery("#" + id).show();
}

jQuery(document).ready(function () {
    jQuery('#scrolling-photo-gallery').jcarousel({
        wrap: "circular",
        scroll: 1,
        initCallback: detailcarousel_initCallback,
        itemVisibleOutCallback: detailcarousel_visibleOutCallback,
        itemVisibleInCallback: { onBeforeAnimation: detailcarousel_visibleInCallback, onAfterAnimation: null }
    });
    
    var visible = getVisibleContentHeight();
    
    if (!document.getElementById("related-items")) {
        // make map the same size as the viewport
        jQuery("#map_canvas").css("height", visible);
    } else if (document.getElementById("map_canvas")) {
        var mapHeight = document.getElementById("map_canvas").clientHeight;
        var relatedHeight = document.getElementById("related-items").clientHeight;
        var diff = visible - (mapHeight + relatedHeight + 30 /* padding */); // adding a little breathing room
        if (diff > 0) {
            jQuery("#map_canvas").css("height", mapHeight + diff);
        }
    }
});

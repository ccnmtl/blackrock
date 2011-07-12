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
        
    var viewportwidth;
    var viewportheight;
    
    // the more standards compliant browsers (mozilla/netscape/opera/IE7) use window.innerWidth and window.innerHeight
    if (typeof window.innerWidth != 'undefined')
    {
         viewportwidth = window.innerWidth,
         viewportheight = window.innerHeight
    }
    else if (typeof document.documentElement != 'undefined'
        && typeof document.documentElement.clientWidth !=
        'undefined' && document.documentElement.clientWidth != 0)
    {
        // IE6 in standards compliant mode (i.e. with a valid doctype as the first line in the document)
        viewportwidth = document.documentElement.clientWidth,
        viewportheight = document.documentElement.clientHeight
    }
    else
    {
        // older versions of IE
        viewportwidth = document.getElementsByTagName('body')[0].clientWidth,
        viewportheight = document.getElementsByTagName('body')[0].clientHeight
    }
    
    var visible = viewportheight - (document.getElementById("mainnav").clientHeight + document.getElementById("brf").clientHeight); 
    
    if (!document.getElementById("related-items")) {
        // make map the same size as the viewport
        jQuery("#map_canvas").css("height", (visible - 20));
    } else {
        var mapHeight = document.getElementById("map_canvas").clientHeight;
        var relatedHeight = document.getElementById("related-items").clientHeight;
        var diff = visible - (mapHeight + relatedHeight + 40 /* padding */); // adding a little breathing room
        if (diff > 0)
            jQuery("#map_canvas").css("height", mapHeight + diff);
    }
});

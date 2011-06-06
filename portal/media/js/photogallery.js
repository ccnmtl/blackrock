function carousel_initCallback(carousel) {
    // Disable autoscrolling if the user clicks the prev or next button.
    jQuery('#toggle_play').bind('click', function() {
        if (carousel.autoStopped) {
            carousel.options.auto = 10;
            carousel.startAuto();
            jQuery(this).removeClass("jcarousel-play");
            jQuery(this).addClass("jcarousel-pause");

            // tell jcarousel to move to the next
            carousel.next();
        } else {
            carousel.stopAuto();
            jQuery(this).removeClass("jcarousel-pause");
            jQuery(this).addClass("jcarousel-play");
        }
    });

    // Link selectors
    jQuery(".jcarousel-selector").bind('click', function() {
        var idx = parseInt(jQuery(this).children('a').html(), 10);
        carousel.scroll(idx, false); 
        carousel.stopAuto();
        jQuery("#toggle_play").removeClass("jcarousel-pause");
        jQuery("#toggle_play").addClass("jcarousel-play");
    });
}

function carousel_visibleOutCallback(carousel, item, pos, action) {
    jQuery(item).children(".jcarousel-caption").hide();
}

function carousel_visibleInCallback(carousel, item, pos, action) {
    jQuery(".jcarousel-selected").removeClass("jcarousel-selected");
    var id = jQuery(item).children('input').val();
    jQuery("#"+id).addClass("jcarousel-selected");
    jQuery(item).children(".jcarousel-caption").show();
}

jQuery(document).ready(function() {
    jQuery('#scrolling-photo-gallery').jcarousel({
        animation: 2000, // fade in/out speed
        fade: 1,
        auto: 10,
        scroll: 1,
        size: 5,
        wrap: "circular",
        initCallback: carousel_initCallback,
        itemVisibleOutCallback: carousel_visibleOutCallback,
        itemVisibleInCallback: { onBeforeAnimation: carousel_visibleInCallback, onAfterAnimation: null }
     });
    
    jQuery('#weather-widget-tab').click(function(event){
        var widget = jQuery("#weather-widget");
        var tab = jQuery('#weather-widget-tab');
        
        if (widget.hasClass('open')) {
            widget.animate({right: "-" + (widget.outerWidth() - tab.outerWidth()) }, 300).removeClass('open');
        } else {
            widget.animate({right:'0'}, 300).addClass('open');
        }
        event.preventDefault();
    });

});

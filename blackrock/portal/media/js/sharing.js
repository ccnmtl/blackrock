/*
 *   enable sharing on all pages of the site
 */

var the_sharing = jQuery.fn.Sharing;

jQuery(document).ready(function () {
    if (typeof(jQuery.fn.Sharing) == "undefined") {
        jQuery.fn.Sharing = the_sharing;
    }
    delete the_sharing; // not caring.
    jQuery.fn.Sharing.websites.twitter = {
        name : 'Twitter',
        image : 'twitter.gif',
        link : 'http://twitter.com/share?url=WEBSITE&amp;via=ccnmtl&amp;text=TITLE'
    };

    jQuery('#sharing_actions').Sharing({
        text : '',
        links : 'facebook,twitter,delicious,googlebookmarks,digg',
        image_dir : '/portal/media/js/jquery.sharing/sharing/',
        image : 'http://upload.wikimedia.org/wikipedia/en/1/10/Black_Rock_Forest_logo.png',
        title : 'I found this fabulous resource at the Black Rock Forest '
    });

    jQuery('#sharing_button').click(function () {
        jQuery('#sharing_actions').toggle();
    });

    // bind a call to google analytics to track share events
    // track both custom event tracking as well as
    // social interaction tracking, for now
    jQuery('.sharing_link').click(function () {
        var tracker = _gat._getTracker('UA-311226-26');

        var url = this.href;

        var category = "Share: " + document.location;
        // var action = url.split('?')[0];
        // pluck out the hostname of the service we are using
        var action = url.split('/')[2];
        // pluck out the section of the portal we are in
        var label = document.location.pathname
                .split('/')[2];

        var now = new Date();
        var value = parseInt(now.getTime(), 10);

        tracker._trackEvent(category, action, label,
                value);

        // http://code.google.com/apis/analytics/docs/tracking/gaTrackingSocial.html
        var network = action;
        var socialAction = 'share';
        var target = document.location;
        _gaq.push(['_trackSocial', network, socialAction, target]);
    });
});
/*
 *   enable sharing on all pages of the site
*/

jQuery(document).ready(function() {
      jQuery.fn.Sharing.websites.twitter = { name: 'Twitter', image: 'twitter.gif', link: 'http://twitter.com/share?url=WEBSITE&amp;via=ccnmtl&amp;text=TITLE' };

      jQuery('#sharing_actions').Sharing({ 
         text: 'Share via:',
         links: 'facebook,twitter,delicious,googlebookmarks,digg', 
         image_dir: '/portal/media/js/jquery.sharing/sharing/',
         image: 'http://upload.wikimedia.org/wikipedia/en/1/10/Black_Rock_Forest_logo.png', 
         title: 'I found this fabulous resource at the Black Rock Forest '
      });
      
      jQuery('#sharing_button').click(function() {
         jQuery('#sharing_actions').toggle('fast', function() {
         // Animation complete.
	 });
      });

    // bind a call to google analytics to track share events 
    jQuery('.sharing_link').click(function() {
	var tracker = _gat._getTracker('UA-311226-26');
	var url = this.href;
	var action = url.split('?')[0];
	var now = new Date();

	//console.log("Share: " + document.location +  ' ' + action + ' '  +  parseInt(now.getTime()));

	tracker._trackEvent("Share: " + document.location,
			    action,
                            String(document.location),
                            parseInt(now.getTime));
    });
});
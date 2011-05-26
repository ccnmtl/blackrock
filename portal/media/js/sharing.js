/*
 *   enable sharing on all pages of the site
*/

jQuery(document).ready(function() {
      jQuery.fn.Sharing.websites.twitter = { name: 'Twitter', image: 'twitter.gif', link: 'http://twitter.com/share?url=WEBSITE&amp;via=ccnmtl&amp;text=TITLE' };

      jQuery('#sharing_actions').Sharing({ 
         text: 'Share me',
         links: 'facebook,twitter,delicious,googlebookmarks,digg', 
         image_dir: '/portal/media/js/jquery.sharing/sharing/',
         image: 'http://upload.wikimedia.org/wikipedia/en/1/10/Black_Rock_Forest_logo.png', 
         title: 'I found this fabulous resource at the Black Rock Forest '
      });
      
      jQuery('#sharing_button').click(function() {
         console.log('enabling sharing button');
         jQuery('#sharing_actions').toggle('fast', function() {
         // Animation complete.
	 });
      });
});
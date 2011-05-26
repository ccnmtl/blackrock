/*
jquery.sharing.js v0.1
Last updated: 31 May 2010

Created by Paulo Cheque
Contact: paulocheque@gmail.com

Licensed under a Creative Commons Attribution-Non-Commercial 3.0 Unported License
http://creativecommons.org/licenses/by-nc/3.0

Example of Usage:
http://plugins.jquery.com/project/Sharing

=SIMPLE USAGE=

// HTML code:
<div id="my_div"></div>

<script type="text/javascript" src="SOME_DIR/js/jquery.sharing.js"></script>

// Default values: { text: 'Sharing: ',
//					 links: 'facebook,delicious,googlebookmarks,twitter,orkut,linkedin,digg,yahoo,live',
// 					 image_dir: '/img/sharing/',
//					 url: '', // default is the current url
//					'image': '', // default is without image. Just some websites support images
//					'title': '', // default is blank. Just some websites support titles
//					}
$('#my_div').Sharing();


=ADD NEW WEBSITES=
// To add new links you can edit the script or just do it before call the function:
// PS: use the WEBSITE keyword to identify where your website will be in the url. 
// PS: use the IMAGE keyword to identify the image used to promote your website.
// PS: use the TITLE keyword to identify the title of your website. 

$.fn.Sharing.websites.facebook = { name: 'Facebook', image: 'facebook.gif', link: 'http://www.facebook.com/share.php?u=WEBSITE' };
$.fn.Sharing.websites.mywebsite = { name: 'MyWebSiteOfSharing', image: 'mysharing.gif', link: 'http://www.example.com/add?u=WEBSITE&img=IMAGE&tt=TITLE' };

Then, it is possible to do this: $('#my_div').Sharing('links': 'facebook,mywebsite');

=CUSTOMIZING=

// Custom values:
$('#my_div').Sharing({ text: '', 
					   links: 'facebook,twitter,delicious,googlebookmarks', 
					   image_dir: '/static/img/sharing/',
					   url: 'http://baladasusp.com',
					   image: 'http://baladasusp.com/static/img/logo.jpg',
					   title: 'Baladas na USP: Veja fotos e videos e fique atento às próximas baladas',
					});

// If you want to customize the layout with CSS:
.sharing_text {}
.sharing_link {}
.sharing_image {}

// Example:
.sharing_text { font-weight: bold; font-size: 10px; }
.sharing_link {}
.sharing_image { width: 15px; height: 15px; margin-right: 5px; }

=TIPS=

// Tip: you can use ImageZoom plugin for a nice effect:
http://plugins.jquery.com/project/SimpleImageZoom

But pay attention with some tricks with:
- jquery animate automatically put a display: block in the image
- Webkit browsers load images with width and height 0px in this case

<script type="text/javascript" src="SOME_DIR/js/jquery.imagezoom.js"></script>

$('#my_div img').ImageZoom();

*/

(function($) {

	$.fn.Sharing = function(options) {
		var properties = $.extend({}, $.fn.Sharing.defaults, options);

		function add_text(div, text) {
			code = "<span class='sharing_text'>" + text + "</span>";
			div.append(code);
		}

		function add_link(div, name, link, image) {
			code = "<a href='" + link + "' class='sharing_link' target='_blank'>" +
						"<img src='" + image + "' title='" + name + "' alt='" + name + "' class='sharing_image'/>" +
					"</a>";
			div.append(code);
		}
		
		function configure_link(original_link, url, image, title) {
    		link = original_link.replace(/WEBSITE/, url);
    		link = link.replace(/IMAGE/, properties.image);
    		link = link.replace(/TITLE/, properties.title);
    		return link;
		}

        return this.each(function(index) {
        	div = $(this);
        	add_text(div, properties.text);
        	links = properties.links.split(',');

        	for(i = 0; i < links.length; i++) {
        		try {
	        		website = $.fn.Sharing.websites[links[i]];
	        		if(properties.url == '') {
	        			url = window.location;
	        		}
	        		else {
	        			url = properties.url;
	        		}
	        		original_link = website.link;
					link = configure_link(original_link, url, properties.image, properties.title);
	        		add_link(div, website.name, link, properties.image_dir + website.image);
	        	} catch(error) {
	        	}
        	}
        });

    }; 
    
	$.fn.Sharing.defaults = {
		'text': 'Sharing: ',
		'links': 'facebook,delicious,googlebookmarks,twitter,orkut,linkedin,digg,live',
		'image_dir': '/img/sharing/',
		'url': '', // default is the current url
		'image': '', // default is without image. Just some websites support images
		'title': '' // default is blank. Just some websites support titles
	};
	
	$.fn.Sharing.websites = {
	 	'facebook': { name: 'Facebook', image: 'facebook.gif', link: 'http://www.facebook.com/share.php?u=WEBSITE' },
		'delicious': { name: 'Del.icio.us', image: 'delicious.gif', link: 'http://del.icio.us/post?url=WEBSITE' },
		'googlebookmarks': { name: 'Google Bookmarks', image: 'google.gif', link: 'http://www.google.com/bookmarks/mark?op=edit&bkmk=WEBSITE&title=TITLE' },
		'twitter': { name: 'Twitter', image: 'twitter.gif', link: 'http://twitter.com/?status=TITLE:WEBSITE' },
		'orkut': { name: 'Orkut', image: 'orkut.gif', link: 'http://promote.orkut.com/preview?nt=orkut.com&du=WEBSITE&tn=IMAGE&tt=TITLE' },
		'linkedin': { name: 'LinkedIn', image: 'linkedin.gif', link: 'http://www.linkedin.com/shareArticle?mini=true&url=WEBSITE' },
		'digg': { name: 'Digg', image: 'digg.gif', link: 'http://digg.com/submit?phase=2&url=WEBSITE' },
		'yahoo': { name: 'Yahoo!', image: 'yahoo.gif', link: 'http://myweb2.search.yahoo.com/myresults/bookmarklet?u=WEBSITE' },
		'live': { name: 'Windows Live', image: 'live.gif', link: 'https://favorites.live.com/quickadd.aspx?marklet=1&mkt=en-us&url=WEBSITE' }
	}
    
})(jQuery);

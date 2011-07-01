
/*******************************************************************
* 
*  constructs an array of the blackrock static web cam images that we pull in every 5 minutes
*
********************************************************************/
// query string processing -  http://snipplr.com/view.php?codeview&id=13239
function getParameterByName( name )
{
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp( regexS );
    var results = regex.exec( window.location.href );
    if( results === null )
	return "";
    else
	return results[1];
}

function get_webcam_image_array(start_date, start_month, start_year, start_hour, start_minute) {
    // ndays_ago =  ndays_ago || 0;
    
    var BASE_IMAGE_URL = "http://ccnmtl.columbia.edu/projects/blackrock/forestdata/webcam";
    var viewer;
    var now = new Date();
    
    var imageObjArray  = [];
    // playing around w/ pulling in last N days
    // for (n = 1; n < 2; n++) {
    // some quick date arithmetic to compute N days ago
    
    var millisecs_per_five_min = 1000*60*5;	
    var millisecs_per_hour = 1000*60*60;	
    var millisecs_per_day = millisecs_per_hour*24;	
    var now_date = new Date(now.getTime());
    
    start_date = start_date || getParameterByName('date') || now_date.getDate();
    start_month = start_month || getParameterByName('month') || now_date.getMonth();
    start_year = start_year || getParameterByName('year') || now_date.getFullYear();
    start_hour = start_hour || getParameterByName('hour') || now_date.getHours();
    start_minute = start_minute || getParameterByName('minute') || now_date.getMinutes();
    
    // console.log("the start_date is:", start_date, start_month, start_year, start_hour, start_minute);
    
    var start_date_object = new Date(start_year, start_month, start_date, start_hour, start_minute);
    var yesterday_date = new Date(start_date_object.getTime() - millisecs_per_day);
    
    /*  count through a 24 hour period, incremending by 5 minutes  (19 / hour * 24 = )cal
	    looping past midnight... e.g. 22,23, 00, 01, 02
	    we will trip over a date (and possibly month/year boundary), so compute date for 
            each incremental hour, and use date arithmatic to get this correct
        */
    // var start_hour = yesterday_date.getHours();
    // using the current minute, round to the nearest 5 minute
    start_minute = Math.round((parseInt(yesterday_date.getMinutes(), 10) / 5)) * 5;
    start_min_date = new Date(yesterday_date.getFullYear(), 
			      yesterday_date.getMonth(), 
			      yesterday_date.getDate(), 
			      yesterday_date.getHours(), 
			      start_minute); 
    
    for (i = 0; i < 288; i++) { 
	// h = (start_hour + i) % 24;
	//console.log("entering main loop: " + i)
	
	current_min_date = new Date(start_min_date.getTime() + (millisecs_per_five_min * i));
	var year =  current_min_date.getFullYear();
	
	// month in our script is 01-12, and starts at 1, not 0
	var month = current_min_date.getMonth() + 1;
	if (month < 10) { 
		month = "0" + month;
	}
	// date is 0 padded in our script, so adjust
	date = current_min_date.getDate();
	if (date < 10) { 
	    date = "0" + date;
	}
	
	var hour = current_min_date.getHours();
	if (hour < 10) { 
	    hour = "0" + hour;
	}
	
	var min = current_min_date.getMinutes();
	if (min < 10) { 
	    min = "0" + min;
	}
	
	//console.log("entering min loop: " + j + "(start_minute, m, min)" + start_minute + ", "  + m + ", " + min);
	    
	path = "/" + year + "/" + month + "/" + date + "/"; 
	image_filename = "Black_Rock_" + hour + "_" + min + ".jpg";
	full_image_path = BASE_IMAGE_URL + path + image_filename;

	thumb_filename = "Black_Rock_" + hour + "_" + min + "_thumb.jpg";
	full_thumb_path = BASE_IMAGE_URL + path + thumb_filename;
	//console.log(image_filename);
	// console.log(full_image_path);
	imageObjArray.push({src: full_image_path,
                            thumb: full_thumb_path,
			    title: image_filename,
		            text:"This photo was taken on " + month + "/" + date + "/" + year + " (" + hour + ":" + min + ")"});
	}
    return imageObjArray;
}

function draw_image_flow(start_date, start_month, start_year, start_hour, start_minute) {

    jQuery('#webcam-flow').empty();

    // add the webcam images to the dom
    var webcamImageArray = get_webcam_image_array(start_date, start_month, start_year, start_hour, start_minute);
    for (i = 0; i < webcamImageArray.length; i++) {
        // console.log(webcamImageArray[i].src);
	jQuery("#webcam-flow").append(
		  jQuery("<img/>")
		    .attr("src", webcamImageArray[i].src)
		    .attr("longdesc", webcamImageArray[i].src)
		    .attr("width", "70")
		    .attr("height", "48")
		    .attr("alt", webcamImageArray[i].text)
		    )
	
    }
    var instanceOne = new ImageFlow();
    // console.log("initializing imageflow");
    instanceOne.init({ ImageFlowID:'webcam-flow',
		       preloadImages: false,
		       //aspectRatio: 2.333, 
		       //aspectRatio: 1, 
		       imageFocusMax: 1,
		       imageFocusM: 1.5,
		       xStep: 220,
		       buttons: true,
		       startID: 287,
		       glideToStartID: false,
               reflections: false,  
               reflectionP: 0.0,
                onClick: function() { return false; }
            });
	
}


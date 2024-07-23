/* global ImageFlow */
/* eslint-disable security/detect-non-literal-regexp, no-useless-escape */
/*******************************************************************************
 *
 * constructs an array of the blackrock static web cam images that we pull in
 * every x minutes
 *
 ******************************************************************************/
// query string processing - http://snipplr.com/view.php?codeview&id=13239
function getParameterByName(name) {
    name = name.replace(/[\[]/, '\\\[').replace(/[\]]/, '\\\]');
    var regexS = '[\\?&]' + name + '=([^&#]*)';
    var regex = new RegExp(regexS);
    var results = regex.exec(window.location.href);
    if (results === null) {
        return '';
    } else {
        return results[1];
    }
}

function get_webcam_image_array(start_date, start_month, start_year,
    start_hour, start_minute) {
    var BASE_IMAGE_URL =
        'https://www1.columbia.edu/sec/ccnmtl/projects/blackrock/forestdata/webcam';
    var now = new Date();
    var interval = 10; // minutes

    var imageObjArray = [];

    var millisecs_per_interval = 1000 * 60 * interval;
    var millisecs_per_hour = 1000 * 60 * 60;
    var millisecs_per_day = millisecs_per_hour * 24;
    var now_date = new Date(now.getTime());

    start_date = start_date || getParameterByName('date') || now_date.getDate();
    start_month = start_month ||
        getParameterByName('month') ||
        now_date.getMonth();

    start_year = start_year ||
        getParameterByName('year') ||
        now_date.getFullYear();

    start_hour = start_hour ||
        getParameterByName('hour') ||
        now_date.getHours();

    start_minute = start_minute ||
        getParameterByName('minute') ||
        now_date.getMinutes();

    var start_date_object =
        new Date(start_year, start_month, start_date, start_hour, start_minute);
    var yesterday_date =
        new Date(start_date_object.getTime() - millisecs_per_day);

    /*
     * count through a 24 hour period, incremending by interval minutes (19 /
     * hour * 24 = )cal looping past midnight... e.g. 22,23, 00, 01, 02 we will
     * trip over a date (and possibly month/year boundary), so compute date for
     * each incremental hour, and use date arithmatic to get this correct
     */
    // var start_hour = yesterday_date.getHours();
    // using the current minute, round to the nearest x minute
    var yest_minutes = parseInt(yesterday_date.getMinutes(), 10);
    start_minute = Math.round((yest_minutes / interval)) * interval;
    var start_min_date = new Date(yesterday_date.getFullYear(),
        yesterday_date.getMonth(), yesterday_date.getDate(),
        yesterday_date.getHours(), start_minute);

    var image_count = (24 * 60) / interval;

    for (var i = 0; i < image_count; i++) {
        var current_min_date = new Date(start_min_date.getTime() +
                                        (millisecs_per_interval * i));
        var year = current_min_date.getFullYear();

        // month in our script is 01-12, and starts at 1, not 0
        var month = current_min_date.getMonth() + 1;
        if (month < 10) {
            month = '0' + month;
        }
        // date is 0 padded in our script, so adjust
        var date = current_min_date.getDate();
        if (date < 10) {
            date = '0' + date;
        }

        var hour = current_min_date.getHours();
        if (hour < 10) {
            hour = '0' + hour;
        }

        var min = current_min_date.getMinutes();
        if (min < 10) {
            min = '0' + min;
        }

        var path = '/' + year + '/' + month + '/' + date + '/';
        var image_filename = 'Black_Rock_' + hour + '_' + min + '.jpg';
        var full_image_path = BASE_IMAGE_URL + path + image_filename;

        var thumb_filename = 'Black_Rock_' + hour + '_' + min + '_thumb.jpg';
        var full_thumb_path = BASE_IMAGE_URL + path + thumb_filename;
        imageObjArray.push({
            src: full_image_path,
            thumb: full_thumb_path,
            title: image_filename,
            text: ' Photo taken at ' + hour + ':' + min
        });
    }
    return imageObjArray;
}

// eslint-disable-next-line no-unused-vars
function draw_image_flow(start_date, start_month, start_year, start_hour,
    start_minute) {
    jQuery('#webcam-flow').empty();

    // add the webcam images to the dom
    var webcamImageArray = get_webcam_image_array(start_date, start_month,
        start_year, start_hour, start_minute);
    var idx = webcamImageArray.length - 1;
    jQuery('#current_image').attr('src', webcamImageArray[idx].src);
    jQuery('#current_image_text').html(webcamImageArray[idx].alt);

    for (var i = 0; i < webcamImageArray.length; i++) {
        jQuery('<img />', {
            'src': webcamImageArray[i].thumb,
            'longdesc': webcamImageArray[i].thumb,
            'width': '125',
            'height': '85',
            'alt': webcamImageArray[i].text
        }).appendTo('#webcam-flow');
    }

    var startIdx = jQuery('div#webcam-flow img').length;


    var imageFlowInstance = new ImageFlow();
    imageFlowInstance.init({
        ImageFlowID: 'webcam-flow',
        imageScaling: true,
        xStep: 125,
        aspectRatio: 4,
        imageFocusMax: 5,
        startID: startIdx,
        glideToStartID: false,
        buttons: true,
        captions: false,
        reflections: false,
        reflectionP: 0.25,
        onClick: function(img) {
            var fullUrl = img && img.src ? img.src: this.src;
            jQuery('#current_image').attr('src',
                fullUrl.replace('_thumb', ''));
            jQuery('#current_image_text').html(img.alt);
        }
    });

    jQuery('#webcam-flow_key').show();
}

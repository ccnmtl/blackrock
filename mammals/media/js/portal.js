function getDisplayHour() {
    var now = new Date();
    var hour = now.getHours();
    var ap = "am";
    if (hour   > 11) { ap = "pm";             }
    if (hour   > 12) { hour = hour - 12;      }
    if (hour   == 0) { hour = 12;             }

    return hour + "" + ap;
}

function getDisplayDate(mydate) {
    var now = mydate;
    if (now == undefined)
        now = new Date();
    var d = now.getDate();
    var day = (d < 10) ? '0' + d : d;
    var m = now.getMonth() + 1;
    var month = (m < 10) ? '0' + m : m;
    var yy = now.getYear();
    
    return month + "/" + day + "/" + now.getFullYear();
}

function getVisibleContentHeight() {
    var viewportwidth;
    var viewportheight;
    
    // the more standards compliant browsers (mozilla/netscape/opera/IE7) use window.innerWidth and window.innerHeight
    if (typeof window.innerWidth != 'undefined') {
         viewportwidth = window.innerWidth,
         viewportheight = window.innerHeight
    } else if (typeof document.documentElement != 'undefined'
        && typeof document.documentElement.clientWidth !=
        'undefined' && document.documentElement.clientWidth != 0) {
        // IE6 in standards compliant mode (i.e. with a valid doctype as the first line in the document)
        viewportwidth = document.documentElement.clientWidth,
        viewportheight = document.documentElement.clientHeight
    } else {
        // older versions of IE
        viewportwidth = document.getElementsByTagName('body')[0].clientWidth,
        viewportheight = document.getElementsByTagName('body')[0].clientHeight
    }
    
    return viewportheight - (10 + document.getElementById("mainnav").clientHeight + document.getElementById("brf").clientHeight); 
}
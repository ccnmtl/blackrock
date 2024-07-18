/* exported getDisplayHour, getDisplayDate, getVisibleContentHeight */

// eslint-disable-next-line no-unused-vars
function getDisplayHour() {
    var now = new Date();
    var hour = now.getHours();
    var ap = 'am';
    if (hour > 11) {
        ap = 'pm';
    }
    if (hour > 12) {
        hour = hour - 12;
    }
    if (hour === 0) {
        hour = 12;
    }

    return hour + '' + ap;
}

// eslint-disable-next-line no-unused-vars
function getDisplayDate(mydate) {
    var now = mydate;
    if (now === undefined) {
        now = new Date();
    }
    var d = now.getDate();
    var day = (d < 10) ? '0' + d : d;
    var m = now.getMonth() + 1;
    var month = (m < 10) ? '0' + m : m;

    return month + '/' + day + '/' + now.getFullYear();
}

// eslint-disable-next-line no-unused-vars
function getVisibleContentHeight() {
    var viewportheight;

    // the more standards compliant browsers (mozilla/netscape/opera/IE7)
    // use window.innerWidth and window.innerHeight
    if (typeof window.innerWidth !== 'undefined') {
        viewportheight = window.innerHeight;
    } else if (typeof document.documentElement !== 'undefined' &&
               typeof document.documentElement.clientWidth !== 'undefined' &&
               document.documentElement.clientWidth !== 0) {
        // IE6 in standards compliant mode
        // (i.e. with a valid doctype as the first line in the document)
        viewportheight = document.documentElement.clientHeight;
    } else {
        // older versions of IE
        viewportheight = document.getElementsByTagName('body')[0].clientHeight;
    }

    var offset = 10 + document.getElementById('mainnav').clientHeight +
        document.getElementById('brf').clientHeight;

    return viewportheight - offset;
}
function getDisplayHour() {
    var now = new Date();
    var hour = now.getHours();
    var ap = "am";
    if (hour   > 11) { ap = "pm";             }
    if (hour   > 12) { hour = hour - 12;      }
    if (hour   == 0) { hour = 12;             }

    return hour + "" + ap;
}

function getDisplayDate() {
    var now = new Date();
    var d = now.getDate();
    var day = (d < 10) ? '0' + d : d;
    var m = now.getMonth() + 1;
    var month = (m < 10) ? '0' + m : m;
    var yy = now.getYear();
    
    return month + "/" + day + "/" + now.getFullYear();
}
function showKey(e) {
    var selectedkey = e.src().id.substr(0, e.src().id.length - 4);
    var keys = ["needle", "pollen", "seed"];
    for (var i = 0; i < keys.length; i++) {
        if (keys[i] === selectedkey) {
            showElement(keys[i] + "-key");
            addElementClass(keys[i] + "-tab", "keytab-selected");
        } else {
            hideElement(keys[i] + "-key");
            removeElementClass(keys[i] + "-tab", "keytab-selected");
        }
    }

    // fix scrolling
    var selected = getFirstElementByTagAndClassName("div",
        "selected", selectedkey + "-key");
    var vertpos = getElementPosition(selected, selectedkey + "-key").y;
    $(selectedkey + "-key").scrollTop =
        $(selectedkey + "-key").scrollTop + vertpos;
}

function getVisibleContentHeight() {
    var viewportwidth;
    var viewportheight;

    // the more standards compliant browsers (mozilla/netscape/opera/IE7) use
    // window.innerWidth and window.innerHeight
    if (typeof window.innerWidth !== 'undefined') {
        viewportheight = window.innerHeight;
    } else if (typeof document.documentElement !== 'undefined' &&
        typeof document.documentElement.clientWidth !== 'undefined' &&
            document.documentElement.clientWidth !== 0) {
        // IE6 in standards compliant mode (i.e. with a valid doctype as the
        // first line in the document)
        viewportheight = document.documentElement.clientHeight;
    } else {
        // older versions of IE
        viewportheight = document.getElementsByTagName('body')[0].clientHeight;
    }
    
    var superHeight = document.getElementById("masthead_top").clientHeight +
        document.getElementById("masthead").clientHeight +
        document.getElementById("instructions").clientHeight +
        document.getElementById("key-tabs").clientHeight +
        65;  /* padding */

    return viewportheight - superHeight;
}

function resize() {
    var height = getVisibleContentHeight();
    var elts = getElementsByTagAndClassName("div", "key");
    forEach(elts, function (elt) {
        setStyle(elt, {'height': height + 'px'});
    });
    
    height -= (15 + document.getElementById("identify-box").clientHeight);
    var elt = document.getElementById("pollen-zoo");
    setStyle(elt, {'height': height + 'px'});
}

function goto(elem) {
    var currenttab = getFirstElementByTagAndClassName("div", "keytab-selected");
    var selectedkey = currenttab.id.substr(0, currenttab.id.length - 4);
    var selected = getFirstElementByTagAndClassName("div",
            "selected", selectedkey + "-key");

    removeElementClass(selected, "selected");
    addElementClass("keyrow-" + selectedkey + elem, "selected");

    // scroll div to the desired element
    var vertpos = getElementPosition("keyrow-" +
            selectedkey + elem, selectedkey + "-key").y;
    $(selectedkey + "-key").scrollTop = $(selectedkey + "-key").scrollTop + vertpos;
}

function resetKey() {
    goto("1");
}

function initKeyNav() {
    connect("pollen-tab", "onclick", showKey);
    connect("needle-tab", "onclick", showKey);
    connect("seed-tab", "onclick", showKey);
    connect("key-reset", "onclick", resetKey);
  
    resize();
  
    connect(window, "onresize", resize);
}

function showTerm(elt) {
    var elts = getElementsByTagAndClassName("div", "morphology-term");
    forEach(elts, function (elt) {
        setStyle(elt, {'display': 'none'});
    });
    var pos = getElementPosition(elt, 'content');
    var id = elt.innerHTML.replace(/\s/gi, "-").toLowerCase();
    setStyle(id, {'top': pos.y + 'px',
                  'left': pos.x + 'px',
                  'display': 'block'});
}

function closeTerm(elt) {
    var parent = getFirstParentByTagAndClassName(elt,
        tagName = 'div',
        className = "morphology-term");
    setStyle(parent, {'display': 'none'});
}

addLoadEvent(initKeyNav);
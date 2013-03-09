var coreHeight = 0;
var zoomedHeight = 0;

function moveSlider() {
    var scrolltop = $("core-zoomed").scrollTop;
    var ratio = scrolltop / zoomedHeight;
    setElementPosition("windowdrag", {
        'y': Math.round(coreHeight * ratio)
    });
}

function coreScroll(elem) {
    var pos = getElementPosition(elem.handle, 'core-unzoomed').y;
    var ratio = pos / coreHeight;
    $("core-zoomed").scrollTop = Math.round(ratio * zoomedHeight);
}

function setupSlider() {
    connect("core-zoomed", "onscroll", moveSlider);

    // we have to use getStyle because getElementDimensions includes the border
    zoomedHeight = $("core-zoomed").scrollHeight -
        parseInt(getStyle("core-zoomed", 'height'), 10);

    var draggerHt = getElementDimensions("windowdrag").h;
    coreHeight = getElementDimensions("core-unzoomed").h - draggerHt;

    new Draggable('windowdrag', {
        snap: function (x, y) {
            var newy = y;
            if (y < 0) {
                newy = 0;
            }
            if (y > coreHeight) {
                newy = coreHeight;
            }
            return [ 0, newy ];
        }
    });
    connect(Draggables, 'drag', coreScroll);
}

addLoadEvent(setupSlider);
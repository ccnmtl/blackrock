var coreHeight = 0;
var zoomedHeight = 0;

function moveSlider() {
  var scrolltop = $("core-zoomed").scrollTop;
  var ratio = scrolltop / zoomedHeight;
  setElementPosition("windowdrag", {'y':coreHeight * ratio});
}

function setupSlider() {
  connect("core-zoomed", "onscroll", moveSlider);

  forEach(getElementsByTagAndClassName("div", "core-slice"), function(elem) {
    //connect(elem, "onclick", moveSlider);
    zoomedHeight += 18.5;  // each core slice is 18px tall.  18.5 works better... it is a mystery.
  });
  
  draggerHt = getElementDimensions("windowdrag").h;
  coreHeight = getElementDimensions("core-unzoomed").h - draggerHt;
}

addLoadEvent(setupSlider);
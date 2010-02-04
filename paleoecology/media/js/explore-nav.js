var coreHeight = 0;
var total = 1070;
var zoomedHeight = 0;

function moveSlider(e) {
  if(e.src().id == "core-zoomed") {   // move from scroll
    var scrolltop = $("core-zoomed").scrollTop;
    var ratio = scrolltop / zoomedHeight;
    setElementPosition("windowdrag", {'y':coreHeight * ratio});
  }
  else { // move to div
    var depth = e.src().id.substr(11);
    setElementPosition("windowdrag", {'y':oneCm * depth});
  }
  //$("windowdrag");
}

function setupSlider() {
  connect("core-zoomed", "onscroll", moveSlider);
  forEach(getElementsByTagAndClassName("div", "core-slice"), function(elem) {
    connect(elem, "onclick", moveSlider);
    zoomedHeight += 18.5;  // each core slice is 18px tall.  18.5 works better... it is a mystery.
  });
  
  coreHeight = getElementDimensions("core-unzoomed").h - 25;  // 25 is the height of the dragger
  oneCm = coreHeight / total;  // size of 1cm of core sample in pixels
}

addLoadEvent(setupSlider);
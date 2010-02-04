var coreHeight = 0;
var total = 1070;

function moveSlider() {
  //$("windowdrag");
}

function moveSliderToDiv(e) {
  var depth = e.src().id.substr(11);
  setElementPosition("windowdrag", {'y':oneCm * depth});
  //$("windowdrag").top = oneCm * depth + "px";
}

function setupSlider() {
  connect("core-zoomed", "onscroll", moveSlider);
  forEach(getElementsByTagAndClassName("div", "core-slice"), function(elem) {
    connect(elem, "onclick", moveSliderToDiv);
  });
  
  coreHeight = getElementDimensions("core-unzoomed").h - 25;  // 25 is the height of the dragger
  oneCm = coreHeight / total;  // size of 1cm of core sample in pixels
}

addLoadEvent(setupSlider);
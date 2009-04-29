function toggle(e) {
  var rightarrow = getFirstElementByTagAndClassName("span", "rightarrow", e.src());
  var downarrow = getFirstElementByTagAndClassName("span", "downarrow", e.src());
  var parent = getFirstParentByTagAndClassName(e.src(), "div", "container");
  var inner = getFirstElementByTagAndClassName("div", "nest", parent);

  var visible = (getStyle(downarrow, "display") != "none");

  if(visible) {
    setStyle(downarrow, {'display':'none'});
    setStyle(rightarrow, {'display':'inline'});
    setStyle(inner, {'display':'none'});
  }
  else {
    setStyle(downarrow, {'display':'inline'});
    setStyle(rightarrow, {'display':'none'});
    setStyle(inner, {'display':'block'});
  }
}

function initToggles() {
  forEach(getElementsByTagAndClassName("h3"), function(elem) {
    connect(elem, "onclick", toggle);
  });
}

addLoadEvent(initToggles);
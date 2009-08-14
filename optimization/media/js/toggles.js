function toggle(e) {
  var rightarrow = getFirstElementByTagAndClassName("span", "rightarrow", e.src());
  var downarrow = getFirstElementByTagAndClassName("span", "downarrow", e.src());
  var parent = getFirstParentByTagAndClassName(e.src(), "div", "toggle-container");
  var inner = getFirstElementByTagAndClassName("div", "toggle-nest", parent);

  var visible = (getStyle(downarrow, "display") != "none");
  log(visible);

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
  forEach(getElementsByTagAndClassName("*", "toggle-control"), function(elem) {
    connect(elem, "onclick", toggle);
  });
}

addLoadEvent(initToggles);
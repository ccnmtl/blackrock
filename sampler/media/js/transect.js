/* global variables */
var transect_length = 20;  // transect length (in meters)

/* set view to given scale */
function initView () {
  $('scale-legend').innerHTML = Math.round(scale * 100) / 100;
  setStyle('scale-bar', {'width':scale});
  drawTrees();
}

/* transect display functions */
function showTransect() {
  // place the transect start in the center of the view
  var startAdjustW = getElementDimensions("transect-start").w * 0.5;
  var startAdjustH = getElementDimensions("transect-start").h * 0.5;
  setStyle("transect-start", {'left':getCenterPx().x - startAdjustW,
                              'top':getCenterPx().y - startAdjustH});

  //$('transect-start-x').value = Math.round((plot_w - treeSize)/2 / scale * 100) / 100;
  //$('transect-start-y').value = Math.round((plot_h - treeSize)/2 / scale * 100) / 100;
  
  $('transect-start-x').value = Math.round(getCenterM().x * 100) / 100;
  $('transect-start-y').value = Math.round(getCenterM().y * 100) / 100;

  // place the transect end
  var endAdjustW = getElementDimensions("transect-end").w * 0.5;
  var endAdjustH = getElementDimensions("transect-end").h * 0.5;

  var x2 = $('transect-end-x').value;
  var y2 = $('transect-end-y').value;

  if(x2 && y2) {
    var endLoc = MetersToPx(x2, y2);
    setStyle("transect-end", {'left':endLoc.x - endAdjustW, 'top':endLoc.y - endAdjustH});
  }
  else {
    //setStyle("transect-end", {'left':center.x - endAdjustW,
    //                          'top':center.y - scale*transect_length - endAdjustH});
    var xLoc = getCenterPx().x;
    var yLoc = getCenterPx().y - scale*transect_length;
    setElementPosition('transect-end', {'x': xLoc - endAdjustW,
                                        'y': yLoc - endAdjustH});
    log("xLoc: " + xLoc + ", yLoc: " + yLoc);
    //$('transect-end-x').value = Math.round((plot_w - treeSize)/2 / scale * 100) / 100;
    //$('transect-end-y').value = Math.round(((plot_h - treeSize)/2 + scale*transect_length) / scale * 100) / 100;
    var adjusted = PxToMeters(xLoc, yLoc);
    log("adjusted: " + adjusted.x + ", " + adjusted.y);
    $('transect-end-x').value = Math.round(adjusted.x * 100) / 100;  
    $('transect-end-y').value = Math.round(adjusted.y * 100) / 100;  
  }
}

function snapTransect(x,y) {
  var new_x = x;
  var new_y = y;

  // length of line between must be transect length
  var transect_ln = scale * transect_length;

  var centerPos = getCenterPx();
  var x1 = centerPos.x;
  var y1 = centerPos.y;

  var adj = MetersToPx($("transect-start-x").value, $("transect-start-y").value)
  var x1 = adj.x;
  var y1 = adj.y;
  
  // get angle toward the user's click
  var theta = Math.atan2(new_y-y1,new_x-x1);

  new_x = x1 + transect_ln * Math.cos(theta);
  new_y = y1 + transect_ln * Math.sin(theta);
  
  // adjust for icon size
  var iconSz = getElementDimensions("transect-end");
  new_x = new_x - 0.5 * iconSz.w;
  new_y = new_y - 0.5 * iconSz.h;

  log(new_x + "," + new_y);
  return [new_x, new_y];
}

function setTransectEnd(e) {
  [x,y] = e.currentDelta();

  // adjust for size of icon
  var adjustX = 0.5 * getElementDimensions("transect-end").w;
  var adjustY = 0.5 * getElementDimensions("transect-end").h;

  var plot_h = getElementDimensions("plot", true).h; 
  var transEnd = PxToMeters(x + adjustX, y + adjustY);
  $('transect-end-x').value = Math.round(transEnd.x * 100) / 100;
  $('transect-end-y').value = Math.round(transEnd.y * 100) / 100;
  //$('transect-end-x').value = Math.round((x + adjustX) / scale * 100) / 100;
  //$('transect-end-y').value = Math.round(((plot_h - treeSize) - (y + adjustY)) / scale * 100) / 100;
  formChanged();
}

function initSelectTransect() {
  new Draggable("transect-end", {'snap':snapTransect});
  connect(Draggables, "end", setTransectEnd);
  showTransect();  // position the transect end point
}

/* form functions */
function formClear() {
  $("transect-start-x").value = "";
  $("transect-start-y").value = "";
  $("transect-end-x").value = "";
  $("transect-end-y").value = "";

  var center = getCenterPx();
  setStyle("transect-start", {'left':center.x - 0.5 * getElementDimensions('transect-start').w,
                              'top':center.y - 0.5 * getElementDimensions('transect-start').h});

  setStyle("transect-end", {'left':center.x - 0.5 * getElementDimensions('transect-end').w,
                            'top':center.y - scale*transect_length - 0.5 * getElementDimensions('transect-end').h});

  var plot_w = getElementDimensions("plot_inner", true).w;
  var plot_h = getElementDimensions("plot_inner", true).h;

  $('transect-start-x').value = Math.round(getCenterM().x * 100) / 100;
  $('transect-start-y').value = Math.round(getCenterM().y * 100) / 100;
  $('transect-end-x').value = Math.round(getCenterM().x * 100) / 100;
  //$('transect-end-y').value = Math.round((getCenterM().y - scale*transect_length) * 100) / 100;
  $('transect-end-y').value = parseFloat($('transect-start-y').value) + 20;

  //$('transect-start-x').value = Math.round((plot_w - treeSize)/2 / scale * 100) / 100;
  //$('transect-start-y').value = Math.round((plot_h - treeSize)/2 / scale * 100) / 100;
  //$('transect-end-x').value = Math.round((plot_w - treeSize)/2 / scale * 100) / 100;
  //$('transect-end-y').value = Math.round(((plot_h - treeSize)/2 + scale*transect_length) / scale * 100) / 100;

  formChanged();
}  

function formSubmit() {
  $('scale').value = scale;

  $('view-width').value = getElementDimensions("plot").w;
  $('view-height').value = getElementDimensions("plot").h;

  $("transect-form").submit();
}
  
function goBack() {
  $("transect-form").action = "plot";
  formSubmit();
}
  
function formChanged() {
  if($("transect-start-x").value != "" && $("transect-start-y").value != "" &&
     $("transect-end-x").value != "" && $("transect-end-y").value != "") {
    $("next").disabled = 0;
  } else {
    $("next").disabled = 1;
  }
  //showTransect();  // shows transect if we already have data
}

function initForm() {
  connect("transect-start-x", "onkeyup", formChanged);
  connect("transect-start-y", "onkeyup", formChanged);
  connect("transect-end-x", "onkeyup", formChanged);
  connect("transect-end-y", "onkeyup", formChanged);
  connect("clear", "onclick", formClear);
  connect("next", "onclick", formSubmit);
  connect("back", "onclick", goBack);
 
  // breadcrumbs
  connect("tab-plot", "onclick", goBack);
  setStyle("tab-plot", {'cursor' : 'pointer'});

  formChanged();   // enables forward button if we already have data
}

addLoadEvent(initView);
addLoadEvent(initSelectTransect);
addLoadEvent(initForm);
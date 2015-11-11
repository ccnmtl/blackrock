var defaultScale = 1;

// this returns the scale that fits all the trees in the view.
function getDefaultScale(max_x, max_y) {
  var xScale = (getElementDimensions("plot").w - treeSize) / max_x;
  var yScale = (getElementDimensions("plot").h - treeSize) / max_y;
  defaultScale = Math.min(xScale, yScale);
}

function updateScale(new_scale) {
  //log("updating scale to " + new_scale);
  scale = new_scale;

  // disallow zooming out when we're already at 100%
  if(scale < defaultScale) {
    scale = defaultScale;
  }

  $('scale-legend').innerHTML = Math.round(scale*100) / 100;
  
  if (scale != undefined) {
      setStyle('scale-bar', {'width':scale});
  }
}

function zoom(factor) {
  if(factor == null) { return; }
  
  var plot_h = getElementDimensions("plot", true).h;

  x_offset = parseInt(getStyle("plot_inner", "left"));
  y_offset = parseInt(getStyle("plot_inner", "top"));

  var current_w = getElementDimensions("plot_inner").w;
  var current_h = getElementDimensions("plot_inner").h;
  
  // do not allow zoom so large that we couldn't fit the transect on (1/2) the screen
  if(factor > ((plot_h - 25) / 40) / scale) {
    factor = ((plot_h - 25) / 40) / scale;
  }
  
  updateScale(scale * factor);

  var new_w = current_w * factor;
  if(new_w < getElementDimensions("plot").w) {
    new_w = getElementDimensions("plot").w;
  }
  var new_h = current_h * factor;
  if(new_h < getElementDimensions("plot").h) {
    new_h = getElementDimensions("plot").h;
  }

  setElementDimensions("plot_inner", {'w':new_w, 'h':new_h});
                                      
  drawTrees();

  var plotSz = getElementDimensions("plot");

  // recenter to original point
  center_x = 0.5 * plotSz.w - x_offset;
  center_y = 0.5 * plotSz.h - y_offset;
  //log("calculated center point (", center_x, ", ", center_y, ").");
  var new_x = 0.5 * plotSz.w - factor * center_x;
  var new_y = 0.5 * plotSz.h - factor * center_y;
  //log("trying new position (", new_x, ", ", new_y, ")...");
  [new_x, new_y] = plotSnapTo(new_x, new_y);
  //log("revised that to (", new_x, ", ", new_y, ")...");
  setStyle("plot_inner", {'left': new_x + 'px', 'top': new_y + 'px'});
}
 
function zoomIn() { zoom(1.5); }

function zoomOut() { zoom(0.67); }

function plotSnapTo(x,y) {
  var view_sz = getElementDimensions("plot", true);
  var plot_sz = getElementDimensions("plot_inner", true);
      
  var new_x = x;
  var new_y = y;
  if(x > 0) { new_x = 0; }
  if(x < view_sz.w - plot_sz.w) { new_x = view_sz.w - plot_sz.w; }
  if(y > 0) { new_y = 0; }
  if(y < view_sz.h - plot_sz.h) { new_y = view_sz.h - plot_sz.h; }
  return [new_x,new_y];
}  

function initPlot() {
  updateScale(defaultScale);
  setElementDimensions("plot_inner", getElementDimensions("plot"));

  var center = getCenterPx();  
  setStyle("transect-start", {'left': center.x - 0.5 * getElementDimensions("transect-start").w,
                              'top': center.y - 0.5 * getElementDimensions("transect-start").h});

  drawTrees();
  new Draggable($("plot_inner"), {'snap':plotSnapTo});
}

function submitForm() {
  $('scale').value = scale;

  $('x-offset').value = parseInt(getStyle("plot_inner", "left"));
  $('y-offset').value = parseInt(getStyle("plot_inner", "top"));
  
  $('view-width').value = getElementDimensions("plot").w;
  $('view-height').value = getElementDimensions("plot").h;

  $('plot-w').value = getElementDimensions("plot_inner").w;
  $('plot-h').value = getElementDimensions("plot_inner").h;

    $('view-form').submit();
}

function setView(x_offset, y_offset, scale_factor, plot_w, plot_h) {
  setElementDimensions("plot_inner", {'w':plot_w, 'h':plot_h});
  updateScale(scale_factor);
  drawTrees();

  setStyle("plot_inner", {"left":x_offset, "top":y_offset});
}

addLoadEvent(initPlot);

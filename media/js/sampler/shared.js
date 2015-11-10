/* global variables */
var scale = 1;
var treeSize = 1;

/* conversions between meters and pixels */
function MetersToPx(x,y) {
  this.x = x * scale;
  this.y = getElementDimensions("plot_inner").h - y * scale - treeSize;
  return this;
}

function PxToMeters(x,y) {
  this.x = x / scale;
  this.y = (-1 * y + getElementDimensions("plot_inner").h - treeSize) / scale;
  //this.y = (-1 * y + getElementDimensions("plot_inner").h) / scale;
  return this;
}

// returns the pixel location of the center point, taking offsets into consideration
function getCenterPx() {
  var plot_w = getElementDimensions("plot", true).w;
  var plot_h = getElementDimensions("plot", true).h;
  
  this.x = plot_w / 2;
  this.y = plot_h / 2;
  return this;
}

function getCenterM() {
  var plot_w = getElementDimensions("plot").w;
  var plot_h = getElementDimensions("plot").h;

  //this.x = (plot_w - treeSize)/2 / scale;
  //this.y = (plot_h - treeSize)/2 / scale;
  log("getCenterPX returns: " + getCenterPx().x + ", " + getCenterPx().y);
  var test = PxToMeters(getCenterPx().x, getCenterPx().y);
  log("returning " + test.x + ", " + test.y);
  return test;
}

function testConversions() {
  var x = 5;
  var y = 2;
  log("setting x to " + x + " and y to " + y + "...");
  //[pxx, pxy] = MetersToPx(x,y);
  newobj = MetersToPx(x,y);
  pxx = newobj.x;
  pxy = newobj.y;
  log("MetersToPx: (" + pxx + ", " + pxy + ")");
  //log("PxToMeters: (" + PxToMeters(pxx, pxy));
  //[old_x, old_y] = PxToMeters(pxx, pxy);
  oldobj = PxToMeters(pxx,pxy);
  log(oldobj.x + ", " + oldobj.y); 
}


function toggle_selected_tree(e) {
  // turn off any previous selection
  var selected = getFirstElementByTagAndClassName("div", "tree-selected");
  if(selected) {
    toggleElementClass("tree-selected", selected);
    toggleElementClass("invisible", "info-" + selected.id);
  }

  // event source was a tree (new selection)
  if ($("info-" + e.src().id) != null) {
      var treeID = e.src().id;
    toggleElementClass("tree-selected", treeID);

    toggleElementClass("invisible", "info-" + treeID);
    //var treePos = getElementPosition(treeID, relativeTo=getElementPosition("plot"));
    //setElementPosition($("info-" + treeID),
    //                   {'x': treePos.x + 50, 'y': treePos.y - 50});
  } // else: event source was an info box (just close it, no new selection)
}

function drawTrees() {
  //log("treeSize: " + treeSize + ", scale: " + scale);
  forEach(getElementsByTagAndClassName("div","tree"), function(tree) {
    var tree_info = $("info-" + tree.id);
    var tree_x = getFirstElementByTagAndClassName("span","info-x",tree_info).innerHTML;
    var tree_y = getFirstElementByTagAndClassName("span","info-y",tree_info).innerHTML;
    setElementPosition(tree, MetersToPx(tree_x, tree_y));
      //setElementPosition(tree_info,
      //                  {'x': x.location.x * scale + 50,
       //                  'y': x.location.y * scale - 125
       //                 });
      connect(tree, "onclick", toggle_selected_tree);
      connect(tree_info, "onclick", toggle_selected_tree);
  });
}

function initTrees() {
  // figure out size of tree icons so we can pad accordingly
  var sampleTree = getFirstElementByTagAndClassName("div", "tree");
  treeSize = Math.max(getElementDimensions(sampleTree).w, getElementDimensions(sampleTree).h);
}

addLoadEvent(initTrees);

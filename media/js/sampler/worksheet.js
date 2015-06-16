xOffset = 0;
yOffset = 0;

/* worksheet functions */
function selectRow(id) {
  // unselect any previous selections
  var prev = getFirstElementByTagAndClassName("tr", "selected");
  if (prev) {
    removeElementClass(prev, "selected");
    removeElementClass("quadrant" + prev.id.substr(3), "selected");
  }
  
  // unselect any selected trees
  var tree = getFirstElementByTagAndClassName("div", "tree-selected");
  if (tree) {
    removeElementClass(tree, "tree-selected");
    addElementClass("info-" + tree.id, "invisible");
  }

  $("radio" + id).checked = 1;
  addElementClass("row" + id, "selected");
  addElementClass("quadrant" + id, "selected");
      
  var treeID = getFirstElementByTagAndClassName("input", "id", "row" + id);
  if(treeID) { signal("tree" + treeID.value, "onclick"); }
}
    
function clearRow(id) {
  var selected_id = getFirstElementByTagAndClassName("input", "id", "row" + id);
  var species = getFirstElementByTagAndClassName("td", "species", "row" + id);
  var dbh = getFirstElementByTagAndClassName("td", "dbh", "row" + id);
  var distance = getFirstElementByTagAndClassName("td", "distance", "row" + id);
  var distanceForm = getFirstElementByTagAndClassName("input", "distance-form", "row" + id);
  var clear = getFirstElementByTagAndClassName("span", "delete", "row" + id);
  selected_id.value = "";
  species.innerHTML = "";
  distance.innerHTML = "";
  distanceForm.value = "";
  dbh.innerHTML = "";
  hideElement(clear);
}
    
function fillIn(e) {
  // if no row is selected, do nothing
  var selected = getFirstElementByTagAndClassName("tr", "selected");
  if (! selected) { return; }

  // get tree id
  var id = e.src().id.substring(4);

  var selected_id = getFirstElementByTagAndClassName("input", "id", selected);
  var species = getFirstElementByTagAndClassName("td", "species", selected);
  var distance = getFirstElementByTagAndClassName("td", "distance", selected);
  var distanceForm = getFirstElementByTagAndClassName("input", "distance-form", selected);
  var dbh = getFirstElementByTagAndClassName("td", "dbh", selected);
  var clear = getFirstElementByTagAndClassName("span", "delete", selected);
      
  //tree = findValue(trees, id);
  selected_id.value = id;
  //species.innerHTML = tree.species;
  species.innerHTML = getFirstElementByTagAndClassName("span", "info-species", "info-tree" + id).innerHTML;
  dbh.innerHTML = getFirstElementByTagAndClassName("span", "info-dbh", "info-tree" + id).innerHTML;

  //distance.innerHTML = getFirstElementByTagAndClassName("span", "info-dbh", "info-tree" + id).innerHTML;
  distance.innerHTML = calculateDistance("quadrant" + selected.id.substr(3), "tree" + id);
  distanceForm.value = distance.innerHTML;
  
  showElement(clear);
}

function calculateDistance(quadrant_id, tree_id) {
  var parent_box = getFirstParentByTagAndClassName(quadrant_id, "div", "box");
  // measure from the center of the box
  var box_x = getElementPosition(parent_box, relativeTo="plot").x + getElementDimensions(parent_box).w / 2;
  var box_y = getElementPosition(parent_box, relativeTo="plot").y + getElementDimensions(parent_box).h / 2;
  //log("quad is centered at: " + box_x + ", " + box_y);
  var tree_x = getElementPosition(tree_id, relativeTo="plot").x;
  // TODO: should invert (since 0,0 is the SW corner)
  var tree_y = getElementPosition(tree_id, relativeTo="plot").y;
  //log("tree is at: " + tree_x + ", " + tree_y);
  var x_length = Math.abs(box_x - tree_x);
  var y_length = Math.abs(box_y - tree_y);
  var dist = Math.sqrt(x_length*x_length + y_length*y_length) / scale;
  //log("distance: " + dist);
  return Math.round(dist * 100) / 100;
}

/* adjust view by old offsets */
function zoomToView() {
  //setStyle("plot_inner", {'left':xOffset, 'top':yOffset});  
  scale = parseFloat($("scale").value);

  //x_offset = parseInt(getStyle("plot_inner", "left"));
  //y_offset = parseInt(getStyle("plot_inner", "top"));
  //x_offset = xOffset;
  //y_offset = yOffset;

  var transectSize = getElementDimensions("transect").h;
  var origScale = scale;
  scale = transectSize / 20;
  var factor = scale / origScale;
  log("calculated factor of " + factor);

  // grow plot
  var currentSz = getElementDimensions("plot_inner");
  setElementDimensions("plot_inner", {'w':currentSz.w * factor, 'h':currentSz.h * factor});

  drawTrees();

  // recenter on original center point
  center_x = 0.5 * getElementDimensions("plot").w;
  center_y = 0.5 * getElementDimensions("plot").h;
  log("calculated center point (", center_x, ", ", center_y, ").");
  
  // adjustment for new scale factor
  var new_x = 0.5 * getElementDimensions("plot").w - factor * center_x;
  var new_y = 0.5 * getElementDimensions("plot").h - factor * center_y;
  
  log("trying new position (", new_x, ", ", new_y, ")...");
  //[new_x, new_y] = plotSnapTo(new_x, new_y);
  //log("revised that to (", new_x, ", ", new_y, ")...");
  setStyle("plot_inner", {'left': new_x + 'px', 'top': new_y + 'px'});

  // now the transect start is located at the bottom of the screen
  var new_x = getElementPosition("transect-start", relativeTo="plot").x + 0.5 * getElementDimensions("transect-start").w;
  var new_y = getElementPosition("transect-start", relativeTo="plot").y + 0.5 * getElementDimensions("transect-start").h;
  log("start transect is at (", new_x, ", ", new_y, ").");
  
  var adjust_x = center_x - new_x;
  var adjust_y = center_y - new_y;
  
  log("adjustment will be (", adjust_x, ", ", adjust_y, ").");
  forEach(getElementsByTagAndClassName("div", "tree"), function(t) {
    var left = getElementPosition(t, relativeTo="plot").x;// + xOffset;
    var top = getElementPosition(t, relativeTo="plot").y;// + yOffset;
    setStyle(t, {'left':left-adjust_x, 'top':top-adjust_y});
  });
  //var new_x = 0.5 * getElementDimensions("plot").w - factor * center_x;
  //var new_y = 0.5 * getElementDimensions("plot").h - factor * center_y;
}

/* form functions */
function goBack() {
  if(confirm("This will clear any worksheet data.  Continue?")) {
    $('back').submit();
  }
}

function plotBack() {
  if(confirm("This will clear your transect selection, as well any worksheet data.  Continue?")) {
    $('back').action = "plot";
    $('back').submit();
  }
}
    
function initWorksheet() {
  //zoomToView();
  //scale = parseFloat($("scale").value);
  //drawTrees();

  forEach(getElementsByTagAndClassName("div", "tree"), function(t) {
    connect(t, "onclick", fillIn);
  });

  // breadcrumbs
  connect("tab-transect", "onclick", goBack); 
  setStyle("tab-transect", {'cursor':'pointer'});
  connect("tab-plot", "onclick", plotBack);
  setStyle("tab-plot", {'cursor':'pointer'});
  
  $('scale-legend').innerHTML = Math.round(scale);
  setStyle('scale-bar', {'width':scale});
}


addLoadEvent(zoomToView);
addLoadEvent(initWorksheet);
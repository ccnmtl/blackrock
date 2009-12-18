var global_http_request;

function showResults(http_request) {
  global_http_request = http_request;

  // store in form for CSV export
  //$('form-results').value = http_request.responseText;  
  //$('csvbutton').disabled = false;
  
  var results = evalJSON(http_request.responseText);
  
  var depth = results['depth'];  // TODO get this from the caller
  var counts = results['counts'];
  
  var row = $('result-row-' + depth);
  
  for(var i=0; i<counts.length; i++) {
    appendChildNodes(row, TD(counts[i], null));
  }
}

function showError(http_request) {
  global_http_request = http_request;
  log(http_request);
  //setStyle('errormessage', {'display':'block'});
  //setStyle('waitmessage', {'display':'none'});
  //$('calculate').disabled = false; 
}

/*function showPlotInfo(plotNumber, results) {
  var parent = $('plot-parent'); 
  var plotTable = $('plot1').innerHTML;
  var id = "plot" + plotNumber;
  var name = "PLOT " + plotNumber;

  if(plotNumber > 1) {
    var newDiv = DIV();
    addElementClass(newDiv, "plot-wrapper");
    addElementClass(newDiv, "toggle-container");
    appendChildNodes(parent, newDiv);
    newDiv.innerHTML = plotTable.replace(/plot1/g, id).replace(/PLOT 1/g, name);
    newDiv.id = id;
    forEach(getElementsByTagAndClassName("tr","calculated",newDiv), function(elem) {
      removeElement(elem);
    });
  }
  $(id+'-area').innerHTML = results['area'];
  $(id+'-time-total').innerHTML = results['time-total'];
  $(id+'-time-travel').innerHTML = results['time-travel'];
  $(id+'-time-locate').innerHTML = results['time-locate'];
  $(id+'-time-establish').innerHTML = results['time-establish'];
  $(id+'-time-measure').innerHTML = results['time-measure'];
  $(id+'-species').innerHTML = results['num-species'];
  $(id+'-count').innerHTML = results['count'];
  $(id+'-details-count').innerHTML = results['count'];
  $(id+'-dbh').innerHTML = results['dbh'];
  $(id+'-variance-dbh').innerHTML = results['variance-dbh'];
  $(id+'-density').innerHTML = results['density'];
  $(id+'-basal').innerHTML = results['basal'];
  
  var numSpecies = results['num-species'];
  var speciesList = results['species-totals'];
  var totalsRow = getFirstElementByTagAndClassName("TR", null, id+'-species-table');
  for(var i=0; i<numSpecies; i++) {
    var child = TR({'class':'calculated'}, TD(null, speciesList[i]['name']),
                         TD({'class':'right'}, speciesList[i]['count']),
                         TD({'class':'right'}, speciesList[i]['dbh']),
                         TD({'class':'right'}, speciesList[i]['variance-dbh']),
                         TD({'class':'right'}, speciesList[i]['density']),
                         TD({'class':'right'}, speciesList[i]['basal'])
                   );
    insertSiblingNodesBefore(totalsRow, child);
  }
  if(plotNumber > 1) {
    var togglectrl = getFirstElementByTagAndClassName("*", "toggle-control", id);
    connect(togglectrl, "onclick", toggle);
  }
}*/

/*
function reset() {
  setStyle('errormessage', {'display':'none'});
  setStyle('waitmessage', {'display':'none'});
  setStyle('results', {'display':'none'});
  setStyle('details', {'display':'none'});
  updateShapeLabel($("plotArrangement"));
  $('csvbutton').disabled = true;
  $('form-results').value = "";
  if(global_http_request) {
    global_http_request.cancel();
  }
  
  forEach(getElementsByTagAndClassName("div","plot-wrapper"), function(elem) {
    if(elem.id != "plot1")
      removeElement(elem);
  });
*/
  /* collapse plot1 if it's un-collapsed */
/*  var rightarrow = getFirstElementByTagAndClassName("span", "rightarrow", "plot1");
  var downarrow = getFirstElementByTagAndClassName("span", "downarrow", "plot1");
  var parent = $("plot1");
  var inner = getFirstElementByTagAndClassName("div", "toggle-nest", parent);

  var visible = (getStyle(downarrow, "display") != "none");

  if(visible) {
    setStyle(downarrow, {'display':'none'});
    setStyle(rightarrow, {'display':'inline'});
    setStyle(inner, {'display':'none'});
  }

}*/


function getResults() {
  //setStyle('waitmessage', {'display':'block'});
  //setStyle('errormessage', {'display':'none'});

  forEach(getElementsByTagAndClassName("tr", "result-row"), function(elem) {
    depth = getFirstElementByTagAndClassName("td", null, elem).innerHTML;

    var params = "depth=" + depth;
    global_http_request = doXHR("getrow", {'method':'POST', 'sendContent':params,
                                         'headers':[["Content-Type", 'application/x-www-form-urlencoded']]
                                          });
    global_http_request.addCallback(showResults);
    global_http_request.addErrback(showError);
  });
}

addLoadEvent(getResults);
var http_request;

function showResults(http_request) {
  var results = evalJSON(http_request.responseText);
  $('results-time').innerHTML = results['sample-time'];

  $('results-variance-density').innerHTML = results['sample-variance-density'];
  $('results-variance-basal').innerHTML = results['sample-variance-basal'];

  $('results-area').innerHTML = results['sample-area'];
  $('results-species').innerHTML = results['sample-species'];
  $('results-count').innerHTML = results['sample-count'];
  $('results-dbh').innerHTML = results['sample-dbh'];
  $('results-density').innerHTML = results['sample-density'];
  $('results-basal').innerHTML = results['sample-basal'];
  $('results-variance-dbh').innerHTML = results['sample-variance-dbh'];

  $('actual-area').innerHTML = results['actual-area'];
  $('actual-species').innerHTML = results['actual-species'];
  $('actual-count').innerHTML = results['actual-count'];
  $('actual-dbh').innerHTML = results['actual-dbh'];
  $('actual-density').innerHTML = results['actual-density'];
  $('actual-basal').innerHTML = results['actual-basal'];
  $('actual-variance-dbh').innerHTML = results['actual-variance-dbh'];
  
  // individual plots
  var plots = results['plots'];
  var numPlots = $('numPlots').value;
  for(var i=0; i<numPlots; i++) {
    showPlotInfo(i+1, plots[i]);
  }

  setStyle('waitmessage', {'display':'none'});
  setStyle('results', {'display':'block'});
  setStyle('details', {'display':'block'});
  $('calculate').disabled = false; 
}

function showError(http_request) {
  //log(http_request);
  setStyle('errormessage', {'display':'block'});
  setStyle('waitmessage', {'display':'none'});
  $('calculate').disabled = false; 
}

function showPlotInfo(plotNumber, results) {
  var parent = $('plot-parent'); 
  var plotTable = $('plot1').innerHTML;
  var id = "plot" + plotNumber;
  var name = "PLOT " + plotNumber;

  if(plotNumber > 1) {
    var newDiv = DIV();
    addElementClass(newDiv, "plot-wrapper");
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
  $(id+'-dbh').innerHTML = results['dbh'];
  $(id+'-density').innerHTML = results['density'];
  $(id+'-basal').innerHTML = results['basal'];
  $(id+'-variance-dbh').innerHTML = results['variance-dbh'];
  
  var numSpecies = results['num-species'];
  var speciesList = results['species-totals'];
  var totalsRow = getFirstElementByTagAndClassName("TR", null, id+'-species-table');
  for(var i=0; i<numSpecies; i++) {
    var child = TR({'class':'calculated'}, TD(null, speciesList[i]['name']),
                         TD({'class':'right'}, speciesList[i]['count']),
                         TD({'class':'right'}, speciesList[i]['dbh']),
                         TD({'class':'right'}, speciesList[i]['density']),
                         TD({'class':'right'}, speciesList[i]['basal']),
                         TD({'class':'right'}, speciesList[i]['variance-dbh'])
                   );
    insertSiblingNodesBefore(totalsRow, child);
  }
}

function reset() {
  setStyle('errormessage', {'display':'none'});
  setStyle('waitmessage', {'display':'none'});
  setStyle('results', {'display':'none'});
  setStyle('details', {'display':'none'});
  $('calculate').disabled = false;
  http_request.cancel();
  
  for(var i=2; i<=10; i++) {
    if($("plot"+i)) {
      removeElement("plot"+i);
    }
  }
}

function validate() {
  // validate number of plots
  var numPlots = $('numPlots').value;
  if(numPlots == "" || isNaN(numPlots)) {
    alert("Error: Number of Plots must be a number.  Please check your input and try again.");
    return false;
  }
  if(numPlots < 1 || numPlots > 100) {
    alert("Error: Number of Plots must be between 1 and 100.  Please check your input and try again.");
    return false;
  }
  if(numPlots.indexOf(".") != -1) {
    alert("Error: Number of Plots must be a whole number.  Please check your input and try again.");
    return false;
  }
  
  // validate plot dimensions
  var size = $('plotSize').value;
  var label = $('shapeLabel').innerHTML;
  if(size == "" || isNaN(size)) {
    alert("Error: Plot " + label + " must be a number.  Please check your input and try again.");
    return false;
  }
  if(size < 1 || size > 100) {
    alert("Error: Plot " + label + " must be between 1 and 100.  Please check your input and try again.");
    return false;
  }
  if(size.indexOf(".") != -1) {
    alert("Error: Plot " + label + " must be a whole number.  Please check your input and try again.");
    return false;
  }  
  
  return true;
}

function calculate() {
  if(! validate()) { return false; }

  $('calculate').disabled = true;
  setStyle('waitmessage', {'display':'block'});
  setStyle('errormessage', {'display':'none'});

  for(var i=2; i<=10; i++) {
    if($("plot"+i)) {
      removeElement("plot"+i);
    }
  }
  
  forEach(getElementsByTagAndClassName("tr","calculated"), function(elem){
    removeElement(elem);
  });

  var numPlots = $('numPlots').value;
  var shape = $('plotShape').value;
  var size = $('plotSize').value;
  var params = "numPlots=" + numPlots + "&shape=" + shape + "&size=" + size;
  http_request = doXHR("calculate", {'method':'POST', 'sendContent':params,
                                         'headers':[["Content-Type", 'application/x-www-form-urlencoded']]
                                        });
  http_request.addCallback(showResults);
  http_request.addErrback(showError);
}

function updateShapeLabel(e) {
  var shape = e.src().value;
  if(shape == "square") {
    $('shapeLabel').innerHTML = "Edge";
  }
  else {
    $('shapeLabel').innerHTML = "Radius";
  }
}

function initRun() {
  connect("calculate", "onclick", calculate);
  connect("reset", "onclick", reset);
  connect("plotShape", "onchange", updateShapeLabel);
}

addLoadEvent(initRun);

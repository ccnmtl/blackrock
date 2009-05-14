var http_request;

function showResults(http_request) {
  var results = evalJSON(http_request.responseText);
  $('results-time').innerHTML = results['results-time'];
  // TODO: sample variance density
  // TODO: sample variance basal area

  // TODO: sample area
  $('results-species').innerHTML = results['results-species'];
  $('results-count').innerHTML = results['results-count'];
  $('results-dbh').innerHTML = results['results-dbh'];
  $('results-density').innerHTML = results['results-density'];
  $('results-basal').innerHTML = results['results-basal'];
  // TODO: sample variance dbh

  $('actual-area').innerHTML = results['actual-area'];
  $('actual-species').innerHTML = results['actual-species'];
  $('actual-count').innerHTML = results['actual-count'];
  $('actual-dbh').innerHTML = results['actual-dbh'];
  $('actual-density').innerHTML = results['actual-density'];
  $('actual-basal').innerHTML = results['actual-basal'];
  $('actual-variance-dbh').innerHTML = results['actual-basal'];
  
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
  }
  $(id+'-area').innerHTML = results['area'];
  $(id+'-time-total').innerHTML = results['time-total'];
  $(id+'-time-travel').innerHTML = results['time-travel'];
  $(id+'-time-locate').innerHTML = results['time-locate'];
  $(id+'-time-establish').innerHTML = results['time-establish'];
  $(id+'-time-measure').innerHTML = results['time-measure'];
  
  $(id+'-count').innerHTML = results['count'];
}

function reset() {
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

function calculate() {
  $('calculate').disabled = true;
  setStyle('waitmessage', {'display':'block'});
  for(var i=2; i<=10; i++) {
    if($("plot"+i)) {
      removeElement("plot"+i);
    }
  }

  var numPlots = $('numPlots').value;
  var shape = $('plotShape').value;
  var diameter = $('plotDiameter').value;
  var params = "numPlots=" + numPlots + "&shape=" + shape + "&diameter=" + diameter;
  http_request = doXHR("calculate", {'method':'POST', 'sendContent':params,
                                         'headers':[["Content-Type", 'application/x-www-form-urlencoded']]
                                        });
  http_request.addCallback(showResults);
}

function initRun() {
  connect("calculate", "onclick", calculate);
  connect("reset", "onclick", reset);
}

addLoadEvent(initRun);
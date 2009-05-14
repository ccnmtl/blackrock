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

  setStyle("waitmessage", {'display':'none'});
  setStyle("results", {'display':'block'});
  setStyle("details", {'display':'block'});
  $('calculate').disabled = false; 
}

function reset() {
  setStyle("results", {'display':'none'});
}

function calculate() {
  $('calculate').disabled = true;
  setStyle("waitmessage", {'display':'block'});
  var numPlots = $('numPlots').value;
  var shape = $('plotShape').value;
  var diameter = $('plotDiameter').value;
  var params = "numPlots=" + numPlots + "&shape=" + shape + "&diameter=" + diameter;
  var http_request = doXHR("calculate", {'method':'POST', 'sendContent':params,
                                         'headers':[["Content-Type", 'application/x-www-form-urlencoded']]
                                        });
  http_request.addCallback(showResults);
}

function initRun() {
  connect("calculate", "onclick", calculate);
  connect("reset", "onclick", reset);
}

addLoadEvent(initRun);
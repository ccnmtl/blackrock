function showResults(http_request) {
  var results = evalJSON(http_request.responseText);
  $('results-time').innerHTML = results['results-time'];
  $('results-species').innerHTML = results['results-species'];
  $('results-count').innerHTML = results['results-count'];
  $('results-living').innerHTML = results['results-living'];
  $('results-dead').innerHTML = results['results-dead'];
  $('results-dbh').innerHTML = results['results-dbh'];
  $('results-density').innerHTML = results['results-density'];
  $('results-basal').innerHTML = results['results-basal'];
  $('actual-density').innerHTML = results['actual-density'];
  $('actual-basal').innerHTML = results['actual-basal'];

  setStyle("waitmessage", {'display':'none'});
  setStyle("results", {'display':'block'});
  $('calculate').disabled = false; 
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
}

addLoadEvent(initRun);
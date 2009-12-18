var global_http_request;

function showResults(http_request) {
  global_http_request = http_request;

  var results = evalJSON(http_request.responseText);
  
  var depth = results['depth'];  // TODO get this from the caller
  var counts = results['counts'];
  
  var row = $('result-row-' + depth);

  var cells = [row.innerHTML];  
  for(var i=0; i<counts.length; i++) {
    cells.push("<td>" + counts[i] + "</td>");
    //appendChildNodes(row, TD(counts[i], null));
  }
  row.innerHTML = cells.join("");
}

function showError(http_request) {
  global_http_request = http_request;
  log(http_request);
  //setStyle('errormessage', {'display':'block'});
  //setStyle('waitmessage', {'display':'none'});
}

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
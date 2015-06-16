var global_http_request;

function showResults(http_request) {
    global_http_request = http_request;

    var results = evalJSON(http_request.responseText);
  
    var depth = results.depth;
    var counts = results.counts;
  
    var row = $('result-row-' + depth);

    var cells = [row.innerHTML];
    for (var i = 0; i < counts.length; i++) {
        cells.push("<td>" + counts[i] + "</td>");
    }
    row.innerHTML = cells.join("");
}

function showError(http_request) {
    global_http_request = http_request;
    log(http_request);
}

function getResults() {
    forEach(getElementsByTagAndClassName("tr", "result-row"), function (elem) {
        var depth = getFirstElementByTagAndClassName("td", null, elem).innerHTML;

        var params = "depth=" + depth;
        global_http_request = doXHR("getrow", {
            'method': 'POST',
            'sendContent': params,
            'headers': [["Content-Type", 'application/x-www-form-urlencoded']]
        });
        global_http_request.addCallback(showResults);
        global_http_request.addErrback(showError);
    });
}

addLoadEvent(getResults);
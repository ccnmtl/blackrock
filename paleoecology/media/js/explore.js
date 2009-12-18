var visible = null;
var global_http_request;

var images = [
  ["Abies", "Alnus", "Asteraceae (incl ragweed)", "Betula", "Carya", "Castanea dentata",
   "Cyperaceae", "Fagus grandifolia", "Fraxinus", "Poaceae", "Ostrya/Carpinus", "Picea",
   "Pinus", "Quercus", "Tsuga canadensis"
  ],
  ["id02.jpg", "id03.jpg", "id04.jpg", "id05.jpg", "id08.jpg", "id09.jpg", "id10.jpg",
   "id11.jpg", "id12.jpg", "id13.jpg", "id14.jpg", "id16.jpg", "id18.jpg", "id19.jpg", "id21.jpg"
  ]
];

function getImage(name) {
  var idx = images[0].indexOf(name);
  return images[1][idx];
}

function showResults(http_request) {
  global_http_request = http_request;

  var results = evalJSON(http_request.responseText);
  
  var depth = results['depth'];  // TODO get this from the caller
  var pollen = results['pollen'];
  var counts = results['counts'];
  var percents = results['percents'];

  var divCounts = $('sample-counts-' + depth);
  var divPercents = $('sample-percents-' + depth);
  
  if(pollen.length == 0) {
    divCounts.innerHTML = "No data.";
    divPercents.innerHTML = "No data.";
    return;
  }
  
  var pctString = "<ul>";
  var countString = "<br />";
  for(var i=0; i<pollen.length; i++) {
    pctString += "<li>"+ pollen[i] + " ("+ percents[i] +"%)</li>";
    var imgString = "<img src='media/images/pollen/" + getImage(pollen[i]) + "'/>"; 
    countString += imgString + "<b>" + pollen[i] + ":</b> " + counts[i] + " grains <br />";
  }
  pctString += "</ul>";
  
  divPercents.innerHTML = pctString;
  divCounts.innerHTML = countString;
}

function showError(http_request) {
  global_http_request = http_request;
  log(http_request);
  //setStyle('errormessage', {'display':'block'});
  //setStyle('waitmessage', {'display':'none'});
}


function showSample(depth) {
  if(visible) { hideElement(visible); }
  visible = $("sample-info-" + depth);
  showElement(visible);
}

function loadResults() {
  //setStyle('waitmessage', {'display':'block'});
  //setStyle('errormessage', {'display':'none'});

  forEach(getElementsByTagAndClassName("div", "sample-info"), function(elem) {
    depth = elem.id.substr(12);

    var params = "depth=" + depth;
    global_http_request = doXHR("getpercents", {'method':'POST', 'sendContent':params,
                                         'headers':[["Content-Type", 'application/x-www-form-urlencoded']]
                                          });
    global_http_request.addCallback(showResults);
    global_http_request.addErrback(showError);
  });
}

addLoadEvent(loadResults);
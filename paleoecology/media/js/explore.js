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
  var otherPercent = results['other'];

  var divCounts = $('sample-counts-' + depth);
  var divPercents = $('sample-percents-' + depth);
  
  if(pollen.length == 0) {
    divCounts.innerHTML = "No data.";
    divPercents.innerHTML = "<ul><li>Other (100%)</li></ul>";
    return;
  }
  
  var pctString = "<ul>";
  var countString = "<br />";
  for(var i=0; i<pollen.length; i++) {
    pctString += "<li>"+ pollen[i] + " ("+ percents[i] +"%)</li>";
    var imgString = "<div class='pollen-zoo-image core'><div id='pollen-image'><img src='media/images/pollen/" + getImage(pollen[i]) + "'/></div>"; 
    countString += imgString + "<div class='imagename'><b>" + pollen[i] + ":</b><br /> " + counts[i] + " grains <br /></div></div>";
  }
  pctString += "<li>Other (" + otherPercent + "%)</li>";
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


function showSample(e) {
  var depth = e.src().id.substr(11);

  if(visible) { hideElement(visible); }
  visible = $("sample-info-" + depth);

  if(! visible) { return; }

  showElement(visible);
  
  // load data as needed
  if(hasElementClass(visible, "unloaded")) {
    var params = "depth=" + depth;
    global_http_request = doXHR("getpercents", {'method':'POST', 'sendContent':params,
                                         'headers':[["Content-Type", 'application/x-www-form-urlencoded']]
                                          });
    global_http_request.addCallback(showResults);
    global_http_request.addErrback(showError);
    removeElementClass(visible, "unloaded");
  }
}

//function loadResults() {
//  forEach(getElementsByTagAndClassName("div", "sample-info"), function(elem) {
//    depth = elem.id.substr(12);

//    var params = "depth=" + depth;
//    global_http_request = doXHR("getpercents", {'method':'POST', 'sendContent':params,
//                                         'headers':[["Content-Type", 'application/x-www-form-urlencoded']]
//                                          });
//    global_http_request.addCallback(showResults);
//    global_http_request.addErrback(showError);
//  });
//}

/* loading all at once is too slow, so load as needed */
//addLoadEvent(loadResults);

function setupCore() {
  forEach(getElementsByTagAndClassName("div", "core-slice"), function(elem) {
    connect(elem, "onclick", showSample);
  });
}

addLoadEvent(setupCore);
var visible = null;
var global_http_request;

var images = [
  ["Abies (Fir)", "Alnus (Alder)", "Asteraceae (Ragweed etc.)", "Betula (Birch)", "Carya (Hickory)", "Castanea dentata (Chestnut)",
   "Cyperaceae (Sedge)", "Fagus grandifolia (Beech)", "Fraxinus (Ash)", "Gramineae (Grasses)", "Ostrya/Carpinus", "Picea (Spruce)",
   "Pinus (Pine)", "Quercus (Oak)", "Tsuga canadensis (Hemlock)"
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
  
  // use Google charts API to create pie chart
  var baseURL = "http://chart.apis.google.com/chart?cht=p"
  var chartSize = "chs=" + "200x400" + "&chdlp=bv";
  var chartLabels = "chdl=";
  //var chartLabels = "chdl=" + pollen.join("|") + "|Other";
  
  //var chartColors = "chco=FF0000,FF69B4,FF8C00,FFFF00,3CB371,00FF00,00FFFF,0000FF,6A5ACD,000000";
  //var chartColors = "chco=FF1F81,A21764,8AB438,999999,3A5B87,00C0C7,C070F0,FF8000,00FF00";
  //var chartColors = "chco=8DD3C7,FFFFB3,BEBADA,FB8072,80B1D3,FDB462,B3DE69,FCCDE5,D9D9D9,BC80BD,CCEBC5,FFED6F";
  var chartColors = "chco=A6CEE3,1F78B4,B2DF8A,33A02C,FB9A99,E31A1C,FDBF6F,FF7F00,CAB2D6,6A3D9A,FFD700,A0522D";
  
  
  if(pollen.length == 0) {
    divCounts.innerHTML = "No data.";
    //divPercents.innerHTML = "<ul><li>Other (100%)</li></ul>";
    divPercents.innerHTML = "";
    
    var imgSrc = baseURL + "&chs=200x200&chd=t:100&chdl=Other (100%)&chdlp=bv";
    $("sample-chart-"+depth).src = imgSrc;
    return;
  }
  
  //var pctString = "<ul>";
  var countString = "<br />";
  for(var i=0; i<pollen.length; i++) {
    //pctString += "<li>"+ pollen[i] + " ("+ percents[i] +"%)</li>";
    var imgString = "<div class='pollen-zoo-image core'><div id='pollen-image'><img src='media/images/pollen/" + getImage(pollen[i]) + "'/></div>"; 
    countString += imgString + "<div class='imagename'><b>" + pollen[i] + ":</b><br /> " + counts[i] + " grains <br /></div></div>";
    chartLabels += pollen[i] + " (" + percents[i] + "%)|";
  }
  //pctString += "<li>Other (" + otherPercent + "%)</li>";
  //pctString += "</ul>";
  
  chartLabels += "Other (" + otherPercent + "%)";
  var chartData = "chd=t:" + percents.join(",") + "," + otherPercent;
  var imgSrc = baseURL + "&" + chartColors + "&" + chartSize + "&" + chartData + "&" + chartLabels;
  $("sample-chart-"+depth).src = imgSrc;
  
  //divPercents.innerHTML = pctString;
  divPercents.innerHTML = "";
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
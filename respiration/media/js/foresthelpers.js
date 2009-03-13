var stations = Array();
var years = Array();

function addYears(stationName, yearlist) {
  stations.push(stationName);
  years.push(yearlist);
}

function updateYears(e) {
  var baseID = e.src().id.split('-')[0]
  var sel = $(baseID + "-year");
  var stationName = e.src().value;

  replaceChildNodes(sel, null);
  for each (year in years[stations.indexOf(stationName)]) {
    appendChildNodes(sel, OPTION({'value':year}, year));
  }
}

function initYearHelper() {
  forEach(getElementsByTagAndClassName("select", "fieldstation-select"), function(elem) {
    connect(elem, "onchange", updateYears);
    var scid = elem.id.split('-')[0];
    for each(year in years[0]) {
      appendChildNodes(scid + "-year", OPTION({'value':year}, year));
    }
  });
}

function calculateKelvin(elem) {
  var parent = getFirstParentByTagAndClassName(elem, "td", null);
  var kelvin = getFirstElementByTagAndClassName("span", "kelvin", parent);
  kelvin.innerHTML = parseFloat(elem.value) + 273.15;
}
function toggle(e) {
  var elem = e.src();
  var parent = getFirstParentByTagAndClassName(elem, "div", "togglecontainer");
  var sibs = getElementsByTagAndClassName("*", "togglechild", parent);
  if(hasElementClass(elem, "toggle-open")) {
    removeElementClass(elem, "toggle-open");
    addElementClass(elem, "toggle-closed");
    forEach(sibs, function(sib) {
            hideElement(sib);
    });
  }
  else {
    removeElementClass(elem, "toggle-closed");
    addElementClass(elem, "toggle-open");
    forEach(sibs, function(sib) {
      showElement(sib);
    });
  }
}

function initNav() {
  connect("tab-forest", "onclick", function() { location.href="leaf";});
  forEach(getElementsByTagAndClassName("div", "toggler"), function(elem) {
          connect(elem, "onclick", toggle);
  });
}

addLoadEvent(initNav);
addLoadEvent(initYearHelper);
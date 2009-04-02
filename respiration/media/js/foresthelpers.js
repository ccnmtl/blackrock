var stations = Array();
var years = Array();

function addYears(stationName, yearlist) {
  stations.push(stationName);
  years.push(yearlist);
}

function updateYears(e) {
  var baseID = e.src().id.split('-')[0];
  var sel = $(baseID + "-year");
  var stationName = e.src().value;

  var selectedYear = sel.value;
  replaceChildNodes(sel, null);
  var yrs = years[stations.indexOf(stationName)];
  for(var i=0; i<yrs.length; i++) {
  //forEach (year in years[stations.indexOf(stationName)]) {
    var year = yrs[i];
    var options = {'value':year};
    if(year == selectedYear) {
      options['selected'] = '';
   }
    appendChildNodes(sel, OPTION(options, year));
  }
}

function initYearHelper() {
  forEach(getElementsByTagAndClassName("select", "fieldstation-select"), function(elem) {
    connect(elem, "onchange", updateYears);
    var scid = elem.id.split('-')[0];
    var selectedYear = $(scid+"-year").value;
    replaceChildNodes(scid+"-year", null);
    for(var i=0; i<years[0].length; i++) {
      var year = years[0][i];
      var options = {'value':year};
      if(year == selectedYear) {
        options['selected'] = '';
      }
      appendChildNodes(scid + "-year", OPTION(options, year));
    }
  });
}

function calculateKelvin(elem) {
  var parent = getFirstParentByTagAndClassName(elem, "td", null);
  var kelvin = getFirstElementByTagAndClassName("span", "kelvin", parent);
  var result = parseFloat(elem.value) + 237.15;
  if(isNaN(result)) {
    kelvin.innerHTML = "";
  }
  else {
    kelvin.innerHTML = result;
  }
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

function submitForm() {
  $('scenario1-species').value = getSpeciesList().join();
  $('scenario1-form').submit();
}

function initNav() {
  connect("tab-leaf", "onclick", submitForm);
  forEach(getElementsByTagAndClassName("div", "toggler"), function(elem) {
          connect(elem, "onclick", toggle);
  });
}

addLoadEvent(initNav);
addLoadEvent(initYearHelper);

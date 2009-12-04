function showPollenKey() {
  hideElement("needle-key");
  hideElement("seed-key");
  showElement("pollen-key");
  removeElementClass("seed-tab", "keytab-selected");
  removeElementClass("needle-tab", "keytab-selected");
  addElementClass("pollen-tab", "keytab-selected");
}

function showNeedleKey() {
  hideElement("pollen-key");
  hideElement("seed-key");
  showElement("needle-key");
  removeElementClass("pollen-tab", "keytab-selected");
  removeElementClass("seed-tab", "keytab-selected");
  addElementClass("needle-tab", "keytab-selected");
}

function showSeedKey() {
  hideElement("needle-key");
  hideElement("pollen-key");
  showElement("seed-key");
  removeElementClass("needle-tab", "keytab-selected");
  removeElementClass("pollen-tab", "keytab-selected");
  addElementClass("seed-tab", "keytab-selected");
}

function initKeyNav() {
  connect("pollen-tab", "onclick", showPollenKey);
  connect("needle-tab", "onclick", showNeedleKey);
  connect("seed-tab", "onclick", showSeedKey);
  connect("key-reset", "onclick", resetKey);
}

function resetKey() {
  var currenttab = getFirstElementByTagAndClassName("div", "keytab-selected");
  var selectedkey = currenttab.id.substr(0, currenttab.id.length-4);
  var selected = getFirstElementByTagAndClassName("table", "selected", selectedkey+"-key");
  removeElementClass(selected, "selected");
  addElementClass("keyitem-"+selectedkey+'1', "selected");
}

function goto(elem2) {
  var currenttab = getFirstElementByTagAndClassName("div", "keytab-selected");
  var selectedkey = currenttab.id.substr(0, currenttab.id.length-4);
  var selected = getFirstElementByTagAndClassName("table", "selected", selectedkey+"-key");
  removeElementClass(selected, "selected");
  addElementClass("keyitem-" + elem2, "selected");
}

addLoadEvent(initKeyNav);
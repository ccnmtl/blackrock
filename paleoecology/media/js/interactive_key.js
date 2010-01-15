function showKey(e) {
  var selectedkey = e.src().id.substr(0, e.src().id.length-4);
  keys = ["needle", "pollen", "seed"];
  for(var i=0; i<keys.length; i++) {
    if(keys[i] == selectedkey) {
      showElement(keys[i]+"-key");
      addElementClass(keys[i]+"-tab", "keytab-selected");
    }
    else {
      hideElement(keys[i]+"-key");
      removeElementClass(keys[i]+"-tab", "keytab-selected");
    }
  }

  // fix scrolling
  var selected = getFirstElementByTagAndClassName("div", "selected", selectedkey+"-key");
  var vertpos = getElementPosition(selected, selectedkey+"-key").y;
  $(selectedkey+"-key").scrollTop = $(selectedkey+"-key").scrollTop + vertpos;
}

function initKeyNav() {
  connect("pollen-tab", "onclick", showKey);
  connect("needle-tab", "onclick", showKey);
  connect("seed-tab", "onclick", showKey);
  connect("key-reset", "onclick", resetKey);
}

function resetKey() {
  goto("1");
}

function goto(elem) {
  var currenttab = getFirstElementByTagAndClassName("div", "keytab-selected");
  var selectedkey = currenttab.id.substr(0, currenttab.id.length-4);
  var selected = getFirstElementByTagAndClassName("div", "selected", selectedkey+"-key");

  removeElementClass(selected, "selected");
  addElementClass("keyrow-" + selectedkey + elem, "selected");

  // scroll div to the desired element
  var vertpos = getElementPosition("keyrow-" + selectedkey + elem, selectedkey+"-key").y;
  $(selectedkey+"-key").scrollTop = $(selectedkey+"-key").scrollTop + vertpos;
}

addLoadEvent(initKeyNav);
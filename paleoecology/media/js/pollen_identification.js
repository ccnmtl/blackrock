var images = [
  ["id01.jpg", "abies (fir) needle", "id01_large.png"],
  ["id02.jpg", "abies (fir) pollen", "id02_large.png"],
  ["id03.jpg", "alnus (alder) pollen", "id03_large.png"],
  ["id04.jpg", "asteraceae (ragweed & herbs) pollen", "id04_large.png"],
  ["id05.jpg", "betula (birch) pollen", "id05_large.png"],
  ["id06.jpg", "betula papyrifera (paper birch) seed", "id06_large.png"],
  ["id07.jpg", "betula populifolia (gray birch) seed", "id07_large.png"],
  ["id08.jpg", "carya (hickory) pollen", "id08_large.png"],
  ["id09.jpg", "castanea dentata (American chestnut) pollen", "id09_large.png"],
  ["id10.jpg", "cyperaceae (sedge) pollen", "id10_large.png"],
  ["id11.jpg", "fagus grandifolia (American beech) pollen", "id11_large.png"],
  ["id12.jpg", "fraxinus (ash) pollen", "id12_large.png"],
  ["id13.jpg", "gramineae (grass) pollen", "id13_large.png"],
  ["id14.jpg", "ostrya/carpinus pollen", "id14_large.png"],
  ["id15.jpg", "picea (spruce) needle", "id15_large.png"],
  ["id16.jpg", "picea (spruce) pollen", "id16_large.png"],
  ["id17.jpg", "pinus strobus (white pine) needle", "id17_large.png"],
  ["id18.jpg", "pinus strobus (white pine) pollen", "id18_large.png"],
  ["id19.jpg", "quercus (oak) pollen", "id19_large.png"],
  ["id20.jpg", "tsuga canadensis (eastern hemlock) needle", "id20_large.png"],
  ["id21.jpg", "tsuga canadensis (eastern hemlock) pollen", "id21_large.png"],
  ["id22.jpg", "ulmus (elm) pollen", "id22_large.png"]
];

var current = -1;

function setup_id_activity() {
  //connect("pollen-choice", "onchange", save_name);
  connect("next", "onclick", display_next_specimen);
  connect("answers", "onclick", check_answers);
  connect("pollen-image", "onclick", show_lightbox);
  connect("pollen-magnify", "onclick", show_lightbox);
  connect("pollen-lightbox-close", "onclick", hide_lightbox);
  connect("pollen-lightbox-content", "onclick", hide_lightbox);
  
  //connect("complete", "onclick", restore);
  addElementClass("content", "unanswered");
}

function setup_zoo() {
  // randomize order of specimens so they don't match the order in the drop-down
  images.sort(function() { return 0.5 - Math.random()});

  var zoo = $("pollen-zoo");
  for(var i=0; i < images.length; i++) {
    var img = IMG({'id':'image'+i, 'src':'media/images/pollen/' + images[i][0]}, null);
    connect(img, "onclick", goto_specimen);
    var namediv = DIV({'class':'imagename', 'id':'image'+i+'-name'}, null);
    var answerdiv = DIV({'class':'imageanswer', 'id':'image'+i+'-answer'}, null);
    appendChildNodes(zoo, DIV({'id':'pollen-zoo-image'+i, 'class':'pollen-zoo-image unanswered'}, img,namediv,answerdiv));
  }

  display_next_specimen();
}

function goto_specimen(e) {
  save_name();
  resetKeys();
  var id = e.src().id;   // imageX
  current = parseInt(id.substr(5));
  replaceChildNodes("pollen-image", IMG({'src':'media/images/pollen/' + images[current][0]}, null));
  $("pollen-image-large").src = 'media/images/pollen/' + images[current][2];
  $('pollen-choice').value = $('image'+current+'-name').innerHTML;
}

function display_next_specimen() {
  save_name();
  resetKeys();
  var nextElem = getFirstElementByTagAndClassName("div", "unanswered", "pollen-zoo");
  if(! nextElem) {
    //$("next").innerHTML = "All species identified.";
    hideElement("next");
    showElement("answers");
  }
  else {
    current = nextElem.id.substr(16);
    replaceChildNodes("pollen-image", IMG({'src':'media/images/pollen/' + images[current][0]}, null));
    $("pollen-image-large").src = 'media/images/pollen/' + images[current][2];
    $('pollen-choice').value = $('image'+current+'-name').innerHTML;

    // scroll div to the desired element
    var vertpos = getElementPosition("pollen-zoo-image"+current, "pollen-zoo").y;
    $("pollen-zoo").scrollTop = $("pollen-zoo").scrollTop + vertpos;
  }
}

function save_name() {
  if(current < 0) { return; }
  var name = $('pollen-choice').value;
  $('image'+current+'-name').innerHTML = name;
  if(name != "") {
    removeElementClass('pollen-zoo-image'+current, 'unanswered');
    addElementClass('pollen-zoo-image'+current, 'answered');
  }
  else {
    addElementClass('pollen-zoo-image'+current, 'unanswered');
    removeElementClass('pollen-zoo-image'+current, 'answered');
  }
}

function check_answers() {
  var nextElem = getFirstElementByTagAndClassName("div", "unanswered", "pollen-zoo");
  if(nextElem) {
    //if(! confirm("You have not chosen an answer for all specimens.  View answer key anyway?")) {
      return;
    //}
  }
  
  swapElementClass('content', 'unanswered', 'answerkey');

  for(var i=0; i<images.length; i++) {
    $('image'+i+'-answer').innerHTML = images[i][1];
  }
  
  forEach(getElementsByTagAndClassName("div", "pollen-zoo-image"), function(elem) {
    var imgtag = elem.id.substr(11);
    var name = $(imgtag+'-name').innerHTML;
    var answer = $(imgtag+'-answer').innerHTML;
    if(name != answer) {
      addElementClass(elem, "wronganswer");
    }
    else {
      addElementClass(elem, "rightanswer");
      hideElement(imgtag+'-answer');
    }
  });
}

function resetKeys () {
  forEach(getElementsByTagAndClassName("div", "key"), function(key) {
    var selected = getFirstElementByTagAndClassName("div", "selected", key);
    var first = getFirstElementByTagAndClassName("div", "keyrow", key);
    if(selected != first) {
      removeElementClass(selected, "selected");
      addElementClass(first, "selected");
      key.scrollTop = 0;  // only works for the currently-selected key :(
    }
  });
}

function show_lightbox () {
    showElement("pollen-lightbox");
    showElement("pollen-lightbox-content");
}

function hide_lightbox () {
    hideElement("pollen-lightbox");
    hideElement("pollen-lightbox-content");
}

addLoadEvent(setup_zoo);
addLoadEvent(setup_id_activity);
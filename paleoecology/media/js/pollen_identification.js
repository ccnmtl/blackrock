var images = [
  ["abies (fir) needle.jpg", "abies (fir) needle"],
  ["abies (fir) pollen.jpg", "abies (fir) pollen"],
  ["alnus (alder) pollen.jpg", "alnus (alder) pollen"],
  ["asteraceae (herbs) pollen.jpg", "asteraceae (herbs) pollen"],
  ["betula (birch) pollen.jpg", "betula (birch) pollen"],
  ["betula papyrifera (paper birch) seed.jpg", "betula papyrifera (paper birch) seed"],
  ["betula populifolia (gray birch) seed.jpg", "betula populifolia (gray birch) seed"],
  ["carya (hickory) pollen.jpg", "carya (hickory) pollen"],
  ["castanea dentata (American chestnut) pollen.jpg", "castanea dentata (American chestnut) pollen"],
  ["cyperaceae (sedge) pollen.jpg", "cyperaceae (sedge) pollen"],
  ["fagus grandifolia (American beech) pollen.jpg", "fagus grandifolia (American beech) pollen"],
  ["fraxinus (ash) pollen.jpg", "fraxinus (ash) pollen"],
  ["gramineae (grass) pollen.jpg", "gramineae (grass) pollen"],
  ["ostrya - carpinus pollen.jpg", "ostrya/carpinus pollen"],
  ["picea (spruce) needle.jpg", "picea (spruce) needle"],
  ["picea (spruce) pollen.jpg", "picea (spruce) pollen"],
  ["pinus strobus (white pine) needle.jpg", "pinus strobus (white pine) needle"],
  ["pinus strobus (white pine) pollen.jpg", "pinus strobus (white pine) pollen"],
  ["quercus (oak) pollen.jpg", "quercus (oak) pollen"],
  ["tsuga canadensis (eastern hemlock) needles.jpg", "tsuga canadensis (eastern hemlock) needles"],
  ["tsuga canadensis (eastern hemlock) pollen.jpg", "tsuga canadensis (eastern hemlock) pollen"]
];

var current = -1;

function setup_id_activity() {
  connect("next", "onclick", save_name);
  connect("answers", "onclick", check_answers);
  connect("closebutton", "onclick", restore);
  connect("identify-form", "onsubmit", form_submit);
}

function setup_zoo() {
  // TODO: randomize order of specimens?
  var zoo = $("pollen-zoo");
  for(var i=0; i < images.length; i++) {
    var img = IMG({'id':'image'+i, 'src':'media/images/pollen/' + images[i][0]}, null);
    connect(img, "onclick", goto_specimen);
    var namediv = DIV({'class':'imagename', 'id':'image'+i+'-name'}, null);
    var answerdiv = DIV({'class':'imageanswer', 'id':'image'+i+'-answer'}, null);
    appendChildNodes(zoo, DIV({'id':'pollen-zoo-image'+i, 'class':'pollen-zoo-image'}, img,BR(),namediv,answerdiv));
  }

  display_next_specimen();
}

function goto_specimen(e) {
  var id = e.src().id;   // imageX
  current = parseInt(id.substr(5));
  replaceChildNodes("pollen-image", IMG({'src':'media/images/pollen/' + images[current][0]}, null));
  $('name-form').value = $('image'+current+'-name').innerHTML;
}

function display_next_specimen() {
  current = current + 1;
  if(current == images.length) {
    $("pollen-image").innerHTML = "";
    $("pollen-writein").innerHTML = "All species identified.";
  }
  else {
    replaceChildNodes("pollen-image", IMG({'src':'media/images/pollen/' + images[current][0]}, null));
    $('name-form').value = $('image'+current+'-name').innerHTML;
  }
}

// this makes the enter key work for moving on to the next specimen
function form_submit(e) {
  e.stop();
  save_name();
}

function save_name() {
  var name = $('name-form').value;
  $('name-form').value = "";
  $('image'+current+'-name').innerHTML = name;
  display_next_specimen();
}

function check_answers() {
  hideElement('right');
  hideElement('identify-box');
  hideElement('instructions');
  $('left').style.paddingRight = 0;
  showElement('closebutton');
  $('zoo-title').innerHTML = "Check Answers";
  
  for(var i=0; i<images.length; i++) {
    $('image'+i+'-answer').innerHTML = images[i][1];
    $('pollen-zoo-image'+i).style.height = "200px";
  }
  
  $('pollen-zoo').style.height = "400px";
  showElement('complete');
}

function restore() {
  hideElement('closebutton');
  $('left').style.paddingRight = "";
  showElement('right');
  showElement('identify-box');
  showElement('instructions');
  $('zoo-title').innerHTML = "Species to Identify";
  forEach(getElementsByTagAndClassName("div", "imageanswer"), function(elem) {
    elem.innerHTML = "";
  });
  forEach(getElementsByTagAndClassName("div", "pollen-zoo-image"), function(elem) {
    elem.style.height = "";
  });
  hideElement('complete');
  $('pollen-zoo').style.height = "";
}

addLoadEvent(setup_zoo);
addLoadEvent(setup_id_activity);
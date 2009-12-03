var images = [
  "abies (fir) needle.jpg",
  "abies (fir) pollen.jpg",
  "alnus (alder) pollen.jpg",
  "asteraceae (herbs) pollen.jpg",
  "betula (birch) pollen.jpg",
  "betula papyrifera (paper birch) seed.jpg",
  "betula populifolia (gray birch) seed.jpg",
  "carya (hickory) pollen.jpg",
  "castanea dentata (American chestnut) pollen.jpg",
  "cyperaceae (sedge) pollen.jpg",
  "fagus grandifolia (American beech) pollen.jpg",
  "fraxinus (ash) pollen.jpg",
  "gramineae (grass) pollen.jpg",
  "ostrya - carpinus pollen.jpg",
  "picea (spruce) needle.jpg",
  "picea (spruce) pollen.jpg",
  "pinus strobus (white pine) needle.jpg",
  "pinus strobus (white pine) pollen.jpg",
  "quercus (oak) pollen.jpg",
  "tsuga canadensis (eastern hemlock) needles.jpg",
  "tsuga canadensis (eastern hemlock) pollen.jpg"
];

var current = -1;

function setup_id_activity() {
  connect("next", "onclick", save_name);
}

function setup_zoo() {
  // TODO: randomize order of specimens?
  var zoo = $("pollen-zoo");
  for(var i=0; i < images.length; i++) {
    var image = images[i];
    var img = IMG({'id':'image'+i, 'src':'media/images/pollen/' + images[i]}, null);
    connect(img, "onclick", goto_specimen);
    var spn = DIV({'class':'imagename', 'id':'image'+i+'-name'}, null);
    appendChildNodes(zoo, DIV({'class':'pollen-zoo-image'}, img,BR(),spn));
  }

  display_next_specimen();
}

function goto_specimen(e) {
  var id = e.src().id;   // imageX
  current = parseInt(id.substr(5));
  replaceChildNodes("pollen-image", IMG({'src':'media/images/pollen/' + images[current]}, null));
  $('name-form').value = $('image'+current+'-name').innerHTML;
}

function display_next_specimen() {
  current = current + 1;
  if(current == images.length) {
    $("pollen-image").innerHTML = "";
    $("pollen-writein").innerHTML = "All species identified.";
  }
  else {
    replaceChildNodes("pollen-image", IMG({'src':'media/images/pollen/' + images[current]}, null));
    $('name-form').value = $('image'+current+'-name').innerHTML;
  }
}

function save_name() {
  var name = $('name-form').value;
  $('name-form').value = "";
  $('image'+current+'-name').innerHTML = name;
  display_next_specimen();
}

addLoadEvent(setup_zoo);
addLoadEvent(setup_id_activity);
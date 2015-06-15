function showArea() {
  var numPlots = $("numPlots").value;
  var shape = $("plotShape").value;
  var size = $("plotSize").value;
  
  if(shape == "square") {
    var area = numPlots * size * size;
  }
  else {
    var area = Math.round(numPlots * Math.PI * (size * size) * 100) / 100;
  }
  $("plotArea").innerHTML = area;  
}

function initArea() {
  connect("numPlots", "onchange", showArea);
  connect("numPlots", "onkeyup", showArea);
  connect("plotShape", "onchange", showArea);
  connect("plotSize", "onchange", showArea);
  connect("plotSize", "onkeyup", showArea);
  showArea();
}

addLoadEvent(initArea);
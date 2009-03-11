function ForestGraphData() {
    //this.Rg = 8.314;  // not used (the database knows this constant)

    this.scenarios = {};
    this.species = {};

    //this.t_a_min = 0; //celsius
    //this.t_a_max = 30;
}

ForestGraphData.prototype.updateScenario = function(scenario_id,color) {
    var obj = this;
    if (typeof(this.scenarios[scenario_id]) == 'undefined') {
      this.scenarios[scenario_id] = {};
    }

    this.scenarios[scenario_id]['name'] = $(scenario_id + "-name").value;
    if (color) {
	this.scenarios[scenario_id]['color'] = color;
	$(scenario_id + "-swatch").style.backgroundColor = color;
    }
    
    this.scenarios[scenario_id].t0 = parseFloat($(scenario_id + "-base-temp").value) + 273.15;
    this.scenarios[scenario_id].leafarea = $(scenario_id + "-leafarea").value;
    this.scenarios[scenario_id].station = $(scenario_id + "-fieldstation").value;
    this.scenarios[scenario_id].start = $(scenario_id + "-startdate").value;
    this.scenarios[scenario_id].end = $(scenario_id + "-enddate").value;
    this.scenarios[scenario_id].deltaT = $(scenario_id + "-delta-t").value;
    if(this.scenarios[scenario_id].deltaT == "")
      this.scenarios[scenario_id].deltaT = 0;

    this.scenarios[scenario_id].valid = false;      
    if(this.scenarios[scenario_id].t0 != "" &&
       this.scenarios[scenario_id].leafarea != "" &&
       this.scenarios[scenario_id].start != "" &&
       this.scenarios[scenario_id].end != ""){
         this.scenarios[scenario_id].valid = true;
    }
    
    forEach(getElementsByTagAndClassName("div", "species", scenario_id), function(elem) {
      obj.updateSpecies(elem.id);
    });
}

ForestGraphData.prototype.updateSpecies = function(species_id) {
    if (typeof(this.species[species_id]) == 'undefined')
      this.species[species_id] = {};
      
    this.species[species_id].valid = false;

    //this.species[species_id]['name'] = $(species_id + "-name").value;
    this.species[species_id]['percent'] = $(species_id + "-percent").value;
    this.species[species_id]['R0'] = $(species_id + "-R0").value;
    this.species[species_id]['E0'] = $(species_id + "-E0").value;
    
    if(this.species[species_id]['R0'] != "" &&
       this.species[species_id]['E0'] != "" &&
       this.species[species_id]['percent'] != "") {
      this.species[species_id].valid = true;
    }
}

// overrides function in graph.js
function initGraph() {
  var g = new Bluff.Bar('graph', 460);
  g.set_theme({
      ///note: not used since we do this in leafGraph() now.
  colors: ['#202020', '#ff1f81', '#a21764', '#8ab438', '#999999', '#3a5b87', 'black'],
    marker_color: '#aea9a9',
    font_color: 'black',
    background_colors: ['white', 'white']
  });
  g.hide_dots = true;
  g.hide_title = true;
  g.x_axis_label = "Scenarios";
  g.sort = false;

  //g.labels = {0: '0', 30: '30'};
  //g.hide_legend = true;  // breaks IE
  //g.hide_line_markers = true;
  g.set_margins(10);
  //g.top_margin = 10;
  //g.bottom_margin = 10;
  g.no_data_message = "Press 'Graph' to graph data.";
  return g;
}

var ForestData = new ForestGraphData();

function updateColors() {
  var colors = ['#ff1f81', '#a21764', '#8ab438', '#999999', '#3a5b87', '#202020'];
  forEach(getElementsByTagAndClassName('div', 'scenario'), function(scenario) {
    var color = colors.shift();
    ForestData.updateScenario(scenario.id,color);
  });
}

function forestGraph() {
    // have to re-init, because g.clear() doesn't reset legend
    //removeElementClass('plotGraph','needsupdate');
    g = initGraph();
    var colors = ['#ff1f81', '#a21764', '#8ab438', '#999999', '#3a5b87', '#202020'];

    forEach(getElementsByTagAndClassName('div', 'scenario'),
       function(scenario) {
         var data = [];
	   var scid = scenario.id;
	   var color = colors.shift();
	   ForestData.updateScenario(scid,color);
	   
	   if(ForestData.scenarios[scid].valid) {

	     var t0 = ForestData.scenarios[scid].t0;
	     var station = ForestData.scenarios[scid].station;
	     var start = ForestData.scenarios[scid].start;
	     var end = ForestData.scenarios[scid].end;
	     var deltaT = ForestData.scenarios[scid].deltaT;

	     var total = 0;

	     forEach(getElementsByTagAndClassName('div', 'species', scenario), function(species) {
	       var species_total = 0;
	     
	       if(ForestData.species[species.id].valid) {
	         var R0 = ForestData.species[species.id].R0;
	         var E0 = ForestData.species[species.id].E0;
	         var http_request = new XMLHttpRequest();
	         var params = "R0="+R0+"&E0="+E0+"&t0="+t0+"&station="+station+"&start="+start+"&end="+end;
	         http_request.open("GET", "getsum?"+params, false);  // blocking AJAX request
	         http_request.send(null);
	         //http_request.send({'R0':R0, 'E0':E0, 't0':t0, 'station':station});
	         //http_request.onreadystatechange = function() {
	         if(http_request.readyState == 4) {
	           if(http_request.status == 200) {
	             var answer = eval("(" + http_request.responseText + ")" );
	             species_total = answer.total;
	           //}// else {
	           //  alert ("AJAX error...");
	           //}
	           }
	           http_request = null;
	         }
	         //};
	         //var d = doXHR("getsum", {'method':'POST',
	         //                                'sendContent':{'R0':R0,
	         //                                               'E0':E0,
	         //                                               't0':t0,
	         //                                               'station':station
	         //                                              }
	         //                               });
	         //d.addCallback( function() { alert(species.id + " returned"); } );
	         //var species_total = 100;
	         var percent = ForestData.species[species.id].percent;
	         total += species_total * (percent/100.0);
	       }
	     });
	     var leafarea = ForestData.scenarios[scid].leafarea;
	     total = total * leafarea;
	     data.push(total);

	     //g.labels = {};
	     //g.labels[LeafData.t_a_min] = LeafData.t_a_min;
	     //g.labels[LeafData.t_a_max] = LeafData.t_a_max;
	     g.data(ForestData.scenarios[scid].name, data, color );
	   }
    });
    g.minimum_value = 0;
    g.draw();
}

// overrides function in graph.js
LeafGraphData.prototype.updateFields = function() {
    return;
    //this.t0 = Number($('kelvin').innerHTML);
    //this.t_a_min = ($('temp_low')) ? Math.round($('temp_low').value) : 0;
    //this.t_a_max = ($('temp_high')) ? Math.round($('temp_high').value) : 30;
}

//EquationHighlighter.prototype.needsUpdate = function() {
	//addElementClass('plotGraph','needsupdate');
//	return;
	//leafGraph();
	//global.TemperatureSliders.updateCursorVals();
//}

addLoadEvent(updateColors);
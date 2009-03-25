function ForestGraphData() {
    //this.Rg = 8.314;  // not used (the database knows this constant)

    this.scenarios = {};
    this.species = {};
    this.colors = ['#ff1f81', '#a21764', '#8ab438', '#999999', '#3a5b87', '#202020'];
    //this.t_a_min = 0; //celsius
    //this.t_a_max = 30;
}

var ForestData = new ForestGraphData();

function showError() { setStyle("error", {'display':'block'}); }

function clearError() { setStyle("error", {'display':'none'}); }

function errorHighlight(elem) {
  addElementClass(elem, "errorHighlight");
  connect(elem, "onfocus", clearHighlight);
  showError();
}

function clearHighlight(e) {
  removeElementClass(e.src(), "errorHighlight");
}

function isLeapYear(year) {
  if(year % 4 == 0) {
    if(year % 100 == 0) {
      if(year % 400 == 0) {
        return true;
      }
      return false;
    }
    return true;
  }
  return false;
}

function isValidMMDD(str, leapyear) {
  var bits = str.split(/[/,-]/);
  if(bits.length != 2) { return false; }
  var month = bits[0];
  var day = bits[1];
  if(month == "" || day == "") {
    return false;
  }
  if(isNaN(month) || isNaN(day)) {
    return false;
  }
  if(month < 1 || month > 12) {
    return false;
  }
  var maxday = 31;
  if(month in {4:'', 6:'', 9:'', 11:''}) { 
     maxday = 30;
  }
  if(month == 2) {
    maxday = 28;   // need to check for leapyears
    if(leapyear) { maxday = 29; }
  }
  if(day < 0 || day > maxday) {
    return false;
  }
  return true;
}

ForestGraphData.prototype.updateScenario = function(scenario_id) {
    var obj = this;
    if (typeof(this.scenarios[scenario_id]) == 'undefined') {
      this.scenarios[scenario_id] = {};
	this.scenarios[scenario_id]['color'] = ForestData.colors.shift();
    }

    this.scenarios[scenario_id]['name'] = $(scenario_id + "-name").value;
    $(scenario_id + "-swatch").style.backgroundColor = this.scenarios[scenario_id]['color'];
    
    var t0 = $(scenario_id + "-base-temp").value;
    if(t0 == "" || isNaN(t0)) {
      errorHighlight(scenario_id + "-base-temp");
      t0 = 0;
    }

    this.scenarios[scenario_id].t0 = parseFloat($(scenario_id + "-base-temp").value) + 273.15;

    var leafarea = $(scenario_id + "-leafarea").value;
    if(leafarea == "" || isNaN(leafarea)) {
      errorHighlight(scenario_id + "-leafarea");
      leafarea = 1;
    }
    this.scenarios[scenario_id].leafarea = leafarea;

    this.scenarios[scenario_id].station = $(scenario_id + "-fieldstation").value;

    var year = $(scenario_id + "-year").value;
    var start = $(scenario_id + "-startdate").value;
    var end = $(scenario_id + "-enddate").value;

    // we'll be nice and allow dashes as well as slashes, even though we say to use "mm/dd".
    start = start.replace("-","/");
    end = end.replace("-","/");

    var dateError = false;
    var leapyear = isLeapYear(year);
    if(! isValidMMDD(start, leapyear)) {
      errorHighlight(scenario_id + "-startdate");
      dateError = true;
    }
    this.scenarios[scenario_id].start = start + "/" + year;

    if(! isValidMMDD(end, leapyear)) {
      errorHighlight(scenario_id + "-enddate");
      this.scenarios[scenario_id].valid = false;
      dateError = true;
    }    
    this.scenarios[scenario_id].end = end + "/" + year;

    /* delta-t is optional */
    this.scenarios[scenario_id].deltaT = $(scenario_id + "-delta-t").value;
    if(this.scenarios[scenario_id].deltaT == "" || isNaN(this.scenarios[scenario_id].deltaT)) {
      // NaN still does indicates an error, since the user tried to enter something
      if(isNaN(this.scenarios[scenario_id].deltaT)) { errorHighlight(scenario_id + "-delta-t"); }
      // but either way, we use 0 for it
      this.scenarios[scenario_id].deltaT = 0;
    }

    var validSpecies = false;  // make sure the scenario contains at least one valid species
    forEach(getElementsByTagAndClassName("div", "species", scenario_id), function(elem) {
      obj.updateSpecies(elem.id);
      if(ForestData.species[elem.id].valid) {
        validSpecies = true;
      }
    });

    // scenarios with missing information are not valid for graphing
    this.scenarios[scenario_id].valid = false;      
    if(this.scenarios[scenario_id].t0 != "" &&
       this.scenarios[scenario_id].leafarea != "" &&
       this.scenarios[scenario_id].start != "" &&
       this.scenarios[scenario_id].end != "" &&
       !dateError &&
       validSpecies){
         this.scenarios[scenario_id].valid = true;
    }
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
  clearError();
  var g = new Bluff.Bar('graph', 460);
  g.set_theme({
      ///note: not used since we do this in leafGraph() now.
    marker_color: '#aea9a9',
    font_color: 'black',
    background_colors: ['white', 'white']
  });
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

function updateColors() {
  clearError();
  forEach(getElementsByTagAndClassName('div', 'scenario'), function(scenario) {
    ForestData.updateScenario(scenario.id);
  });
}

function forestGraph() {
    // have to re-init, because g.clear() doesn't reset legend
    //removeElementClass('plotGraph','needsupdate');
    g = initGraph();
    var scenario_count = 0;

    forEach(getElementsByTagAndClassName('div', 'scenario'),
       function(scenario) {
         var data = [];
	   var scid = scenario.id;
	   ForestData.updateScenario(scid);
	   
	   if(ForestData.scenarios[scid].valid) {
	     scenario_count++;  // closure
	     //log(scenario_count);

	     var t0 = ForestData.scenarios[scid].t0;
	     var station = ForestData.scenarios[scid].station;
	     var start = ForestData.scenarios[scid].start;
	     var end = ForestData.scenarios[scid].end;
	     var deltaT = ForestData.scenarios[scid].deltaT;
           var leafarea = ForestData.scenarios[scid].leafarea;

	     data[scenario_count-1] = 0;
           var species_count = 0; // closure

	     forEach(getElementsByTagAndClassName('div', 'species', scenario), function(species) {
	       if(ForestData.species[species.id].valid) {
	         species_count++;
	         var R0 = ForestData.species[species.id].R0;
	         var E0 = ForestData.species[species.id].E0;
               var percent = ForestData.species[species.id].percent;
	         var params = "R0="+R0+"&E0="+E0+"&t0="+t0+"&station="+station+"&start="+start+"&end="+end+"&delta="+deltaT;
	         var http_request = doXHR("getsum", {'method':'POST', 'sendContent':params,
	                                             'headers':[["Content-Type", 'application/x-www-form-urlencoded']]
	                                            });

	         
	         function my_callback(scenario_num,scid,percent,http_request) {
  	           var answer = evalJSON(http_request.responseText);
  	           //log(data[scenario_num-1]);
	           data[scenario_num-1] += answer.total * (percent/100.0);
	           species_count--;
	           //log(data[scenario_num-1],answer.total);
                 if(species_count == 0) {  // got all species totals for this scenario
	             data[scenario_num-1] = data[scenario_num-1] * leafarea;
	             g.data(ForestData.scenarios[scid].name, data[scenario_num-1], ForestData.scenarios[scid]['color'] );
	             scenario_count--;
	             //log(scenario_count);
                 
	             if(scenario_count == 0) {   // that's all, folks
	                   g.minimum_value = 0;
	                   g.draw();
	             }
	           }
	         }
	         http_request.addCallback(partial(my_callback,scenario_count,scid,percent)); 

	         //total += species_total * (percent/100.0);
	       }
	     });
	     //data.push(total);

	     //g.data(ForestData.scenarios[scid].name, data, ForestData.scenarios[scid]['color'] );
	   }
    });
    //g.minimum_value = 0;
    //g.draw();
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
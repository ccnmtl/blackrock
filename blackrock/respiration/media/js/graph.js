function LeafGraphData() {
    this.Rg = 8.314;
    this.species = {};
    // This is now part of species
    //this.t0 = null; //base temp
    this.t_a_min = 0; //celsius
    this.t_a_max = 30;

    this.colors = ['#ff1f81', '#a21764', '#8ab438', '#999999', '#3a5b87', '#00c0c7', '#c070f0', '#ff8000', '#00ff00'];
}

var LeafData = new LeafGraphData();

LeafGraphData.prototype.updateSpecies = function(species_id) {
    if (typeof(this.species[species_id]) == 'undefined') {
      this.species[species_id] = {};
      var color = this.species[species_id].color = LeafData.colors.shift();
      if( typeof( color ) == 'undefined' ) {  // if we run out of colors, cycle them
        LeafData.colors = ['#ff1f81', '#a21764', '#8ab438', '#999999', '#3a5b87', '#00c0c7', '#c070f0', '#ff8000', '#00ff00'];
        this.species[species_id].color = LeafData.colors.shift();
      }
    }

    this.species[species_id].name = $(species_id + "-name").value;
    this.species[species_id].t0 = $(species_id + "-base-temp").value;
    this.species[species_id].R0 = $(species_id + "-R0").value;
    this.species[species_id].E0 = $(species_id + "-E0").value;
    $(species_id + "-swatch").style.backgroundColor = this.species[species_id].color;
};

function updateColors() {
  forEach(getElementsByTagAndClassName('div', 'species'), function(species) {
    LeafData.updateSpecies(species.id);
  });
}

LeafGraphData.prototype.updateFields = function() {
    var min = ($('temp_low')) ? Math.round($('temp_low').value * 100) / 100 : 0;
    var max = ($('temp_high')) ? Math.round($('temp_high').value * 100) / 100 : 30;
    
    if (max < 0 || max > 45) {
        $('temp_high').focus();
        alert("Please change the maximum temperature value. Valid temperature ranges are between 0C and 45C");
        $('temp_high').value = 30;
        return false;
    } else if (min < 0 || min > 45) {
        $('temp_low').focus();
        alert("Please change the minimum temperature value. Valid temperature ranges are between 0C and 45C");
        $('temp_low').value = 0;
        return false;
    }  else if (min > max) {
        $('temp_low').focus();
        alert("The minimum temperature must be less than the maximum temperature");
        $('temp_low').value = 0;
        $('temp_high').value = 30;
        return false;
    } 

    // Temperature now associated with species
    //this.t0 = Number($('kelvin').innerHTML);
    this.t_a_min = min;
    this.t_a_max = max;
    return true;
};

//what is t_a?
LeafGraphData.prototype.arrhenius = function(species_id, t_a) {
    var data = this.species[species_id];
    if ((! data.base-temp) || (isNaN(data.base-temp))) {
    throw "Please set a valid base temperature.";
    }
    if((! data.R0) || (! data.E0) || (isNaN(data.R0)) || (isNaN(data.E0))) {
    throw "Please set valid R0 and E0 values for "+data.name;
    }
    var Rval = arrhenius(data.R0, data.E0, this.Rg, data.base-temp, t_a+273.15);
//    if ((! data.t0) || (isNaN(data.t0))) {
//    throw "Please set a valid base temperature.";
//    }
//    if((! data.R0) || (! data.E0) || (isNaN(data.R0)) || (isNaN(data.E0))) {
//    throw "Please set valid R0 and E0 values for "+data.name;
//    }
//    var Rval = arrhenius(data.R0, data.E0, this.Rg, data.t0, t_a+273.15);
    return Rval;
};

function leafGraph() {
    // have to re-init, because g.clear() doesn't reset legend
    if ($("plotGraph") === null) {
        return false; 
    }
    if (!LeafData.updateFields()) {
        return false;
    }
    removeElementClass('plotGraph', 'needsupdate');
    g = initGraph();
    

    forEach(getElementsByTagAndClassName('div', 'species'),
       function(species) {
       var spid = species.id;
       var data = [];
       //var color = colors.shift();
       LeafData.updateSpecies(spid);

       g.labels = {};
       //#54006 (LEAF) Remove x-axis labels...
       //g.labels[LeafData.t_a_min] = LeafData.t_a_min;
       //g.labels[LeafData.t_a_max] = LeafData.t_a_max;
       for(var i=LeafData.t_a_min; i<=LeafData.t_a_max; i++) {
           try {
           var Rval = LeafData.arrhenius(spid, i);
           if (!isNaN(Rval)) {
               data.push(Rval);
               //if(Rval > 0) { g.left_margin = 0; }
           }
           } catch(e) {
           g = initGraph();//re-init in case we already added data
           g.no_data_message = e;
           g.draw();
           throw "non valid data";
           }
       }


       g.data(LeafData.species[spid].name, data, LeafData.species[spid].color);

       });
  //g.data('Oaks', [1, 2, 3, 4, 4, 3]);
  //g.data('Maples', [4, 8, 7, 9, 8, 9]);
  g.draw();
  return true;
}


function arrhenius(R0, E0, Rg, base-temp, Ta) {
    var inner = ( (1/base-temp) - (1/Ta));
    var right = (E0 / Rg) * inner;
    var Rval = R0 * Math.exp(right);
    return Math.round(Rval*1000)/1000; //3 decimals
}

function initGraph() {
  var g = new Bluff.Line('graph', "460x345");
  g.set_theme({
    marker_color: '#aea9a9',
    font_color: 'black',
    background_colors: ['white', 'white']
  });
  g.hide_dots = true;
  g.hide_title = true;
  g.x_axis_label = "Ambient Temperature (Ta)";

  //g.labels = {0: '0', 30: '30'};
  //g.hide_legend = true;  // breaks IE
  //g.hide_line_markers = true;
  g.set_margins(0);
  g.left_margin = 30;
  g.top_margin = 10;
  g.right_margin = 5;
  g.bottom_margin = 10;
  g.no_data_message = "";
  g.no_data_font_size = 32;
  return g;
}

function setup() {
  var g = initGraph();
  g.draw();
}


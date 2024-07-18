/* exported leafGraph, setup, LeafData */
/* global Bluff: true */

function LeafGraphData() {
    this.Rg = 8.314;
    this.species = {};
    this.t_a_min = 0;
    this.t_a_max = 30;
    this.colors = [
        '#ff1f81', '#a21764', '#8ab438', '#999999', '#3a5b87',
        '#00c0c7', '#c070f0', '#ff8000', '#00ff00'];
}

var LeafData = new LeafGraphData();

LeafGraphData.prototype.updateSpecies = function(species_id) {
    if (typeof(this.species[species_id]) == 'undefined') {
        this.species[species_id] = {};
        var color = this.species[species_id].color = LeafData.colors.shift();
        if (typeof(color) == 'undefined') {
            LeafData.colors = [
                '#ff1f81', '#a21764', '#8ab438', '#999999', '#3a5b87',
                '#00c0c7', '#c070f0', '#ff8000', '#00ff00'];
            this.species[species_id].color = LeafData.colors.shift();
        }
    }

    this.species[species_id].name = $(species_id + '-name').value;
    this.species[species_id].basetemp = $(species_id + '-base-temp').value;
    this.species[species_id].kelvin = $(species_id + '-kelvin').value;
    this.species[species_id].R0 = $(species_id + '-R0').value;
    this.species[species_id].E0 = $(species_id + '-E0').value;
    //works as advertised
};

LeafGraphData.prototype.updateFields = function() {
    var min =
        ($('temp_low')) ? Math.round($('temp_low').value * 100) / 100 : 0;
    var max =
        ($('temp_high')) ? Math.round($('temp_high').value * 100) / 100 : 30;

    if (max < 0 || max > 45) {
        $('temp_high').focus();
        alert('Please change the maximum temperature value. Valid ' +
              'temperature ranges are between 0C and 45C');
        $('temp_high').value = 30;
        return false;
    } else if (min < 0 || min > 45) {
        $('temp_low').focus();
        alert('Please change the minimum temperature value. Valid ' +
              'temperature ranges are between 0C and 45C');
        $('temp_low').value = 0;
        return false;
    }  else if (min > max) {
        $('temp_low').focus();
        alert('The minimum temperature must be less than ' +
              'the maximum temperature');
        $('temp_low').value = 0;
        $('temp_high').value = 30;
        return false;
    }

    this.t_a_min = min;
    this.t_a_max = max;
    return true;
};


LeafGraphData.prototype.arrhenius = function(species_id, t_a) {
    var data = this.species[species_id];

    if ((! data.basetemp) || (isNaN(data.basetemp))) {
        throw 'Please set a valid base temperature.';
    }
    if ((! data.R0) || (! data.E0) || (isNaN(data.R0)) || (isNaN(data.E0))) {
        throw 'Please set valid R0 and E0 values for '+data.name;
    }

    data.basetemp = parseInt(data.basetemp, 10);
    return arrhenius(
        data.R0, data.E0, this.Rg, data.basetemp + 273.15, t_a + 273.15);
};


// eslint-disable-next-line no-unused-vars
function leafGraph() {
    // have to re-init, because g.clear() doesn't reset legend
    if ($('plotGraph') === null) {
        return false;
    }

    if (!LeafData.updateFields()) {
        return false;
    }
    removeElementClass('plotGraph', 'needsupdate');

    var g = initGraph();

    forEach(getElementsByTagAndClassName('div', 'species'),
        function(species) {
            var spid = species.id;
            var data = [];
            LeafData.updateSpecies(spid);

            g.labels = {};

            for (var i=LeafData.t_a_min; i<=LeafData.t_a_max; i++) {

                try {
                    var Rval = LeafData.arrhenius(spid, i);
                    if (!isNaN(Rval)) {
                        data.push(Rval);
                    }
                } catch (e) {
                    g = initGraph();//re-init in case we already added data
                    g.no_data_message = e;
                    g.draw();
                    throw 'non valid data';
                }
            }

            g.data(LeafData.species[spid].name, data,
                LeafData.species[spid].color);
        });

    g.draw();
    return true;
}

function arrhenius(R0, E0, Rg, basetemp, Ta) {
    var inner = ((1/basetemp) - (1/Ta));
    var right = (E0 / Rg) * inner;
    var Rval = R0 * Math.exp(right);
    return Math.round(Rval*1000)/1000;
}


function initGraph() {
    var g = new Bluff.Line('graph', '460x345');
    g.set_theme({
        marker_color: '#aea9a9',
        font_color: 'black',
        background_colors: ['white', 'white']
    });
    g.hide_dots = true;
    g.hide_title = true;
    g.x_axis_label = 'Ambient Temperature (Ta)';
    g.set_margins(0);
    g.left_margin = 30;
    g.top_margin = 10;
    g.right_margin = 5;
    g.bottom_margin = 10;
    g.no_data_message = '';
    g.no_data_font_size = 32;
    return g;
}

// eslint-disable-next-line no-unused-vars
function setup() {
    var g = initGraph();
    g.draw();
}

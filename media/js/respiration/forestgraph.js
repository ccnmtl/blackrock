/* global Bluff: true, initGraph: true, LeafGraphData: true */
/* exported forestGraph, setupForest, calculateKelvin, makeExportLink */
/* exported clearError, ForestData */

function ForestGraphData() {
    this.scenarios = {};
    this.species = {};
    this.colors = [
        '#ff1f81', '#a21764', '#8ab438', '#999999', '#3a5b87',
        '#00c0c7', '#c070f0', '#ff8000', '#00ff00'];
    /* adding things here to experiment */
    this.showError;
    this.clearError;
    this.errorHighlight;
    this.clearHighlight;
}

var ForestData = new ForestGraphData();

function showError() {
    setStyle('error', {'display': 'block'});
}

function clearError() {
    setStyle('error', {'display': 'none'});
}

function errorHighlight(elem) {
    addElementClass(elem, 'errorHighlight');
    connect(elem, 'onfocus', clearHighlight);
    showError();
}

function clearHighlight(e) {
    removeElementClass(e.src(), 'errorHighlight');
}

function isLeapYear(year) {
    if (year % 4 === 0) {
        if (year % 100 === 0) {
            if (year % 400 === 0) {
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
    if (bits.length != 2) {
        return false;
    }
    var month = bits[0];
    var day = bits[1];
    if (month === '' || day === '') {
        return false;
    }
    if (isNaN(month) || isNaN(day)) {
        return false;
    }
    month = parseInt(month, 10);
    day = parseInt(day, 10);
    if (month < 1 || month > 12) {
        return false;
    }
    var maxday = 31;
    if ([4, 6, 9, 11].indexOf(month) > -1) {
        maxday = 30;
    }
    if (month === 2) {
        maxday = 28;   // need to check for leapyears
        if (leapyear) {
            maxday = 29;
        }
    }
    if (day < 0 || day > maxday) {
        return false;
    }
    return true;
}

ForestGraphData.prototype.updateScenario = function(scenario_id) {
    var obj = this;

    if (typeof(this.scenarios[scenario_id]) == 'undefined') {
        this.scenarios[scenario_id] = {};
        var color =
            this.scenarios[scenario_id].color = ForestData.colors.shift();
        if (typeof(color) == 'undefined') {
            // if we run out of colors, cycle them
            ForestData.colors = [
                '#ff1f81', '#a21764', '#8ab438', '#999999', '#3a5b87',
                '#00c0c7', '#c070f0', '#ff8000', '#00ff00'];
            this.species[scenario_id].color = ForestData.colors.shift();
        }
    }

    this.scenarios[scenario_id].name =
        $(scenario_id + '-name').value.replace(/^\s*|\s*$/,'');
    $(scenario_id + '-swatch').style.backgroundColor =
        this.scenarios[scenario_id].color;

    var leafarea = $(scenario_id + '-leafarea').value;
    if (leafarea === '' || isNaN(leafarea)) {
        errorHighlight(scenario_id + '-leafarea');
        leafarea = 1;
    }
    this.scenarios[scenario_id].leafarea = leafarea;
    this.scenarios[scenario_id].station =
        $(scenario_id + '-fieldstation').value;
    var year = $(scenario_id + '-year').value;
    var start = $(scenario_id + '-startdate').value;
    var end = $(scenario_id + '-enddate').value;


    // we'll be nice and allow dashes as well as slashes,
    // even though we say to use "mm/dd".
    start = start.replace('-','/');
    end = end.replace('-','/');

    var dateError = false;
    var leapyear = isLeapYear(year);
    if (! isValidMMDD(start, leapyear)) {
        errorHighlight(scenario_id + '-startdate');
        dateError = true;
    }
    this.scenarios[scenario_id].start = start + '/' + year;

    if (! isValidMMDD(end, leapyear)) {
        errorHighlight(scenario_id + '-enddate');
        this.scenarios[scenario_id].valid = false;
        dateError = true;
    }
    this.scenarios[scenario_id].end = end + '/' + year;

    /* delta-t is optional */
    this.scenarios[scenario_id].deltaT =
        $(scenario_id + '-delta-t').value;
    if (this.scenarios[scenario_id].deltaT === '' ||
            isNaN(this.scenarios[scenario_id].deltaT)) {
        // NaN still does indicates an error,
        // since the user tried to enter something
        if (isNaN(this.scenarios[scenario_id].deltaT)) {
            errorHighlight(scenario_id + '-delta-t');
        }
        // but either way, we use 0 for it
        this.scenarios[scenario_id].deltaT = 0;
    }

    var species_composition = 0;
    var species_valid = true;
    forEach(getElementsByTagAndClassName('div', 'species', scenario_id),
        function(elem) {
            obj.updateSpecies(elem.id);
            if (!ForestData.species[elem.id].valid) {
                species_valid = false;
            } else {
                species_composition +=
                    parseInt(ForestData.species[elem.id].percent, 10);
            }
        }
    );

    // scenarios with missing information are not valid for graphing
    this.scenarios[scenario_id].valid =
        this.scenarios[scenario_id].leafarea !== '' &&
        this.scenarios[scenario_id].start !== '' &&
        this.scenarios[scenario_id].end !== '' &&
        !dateError &&
        species_valid &&
        species_composition === 100;
};

ForestGraphData.prototype.updateSpecies = function(species_id) {
    if (typeof(this.species[species_id]) == 'undefined')
        this.species[species_id] = {};
    this.species[species_id].valid = false;
    this.species[species_id].name = $(species_id + '-name').value;
    this.species[species_id].basetemp = $(species_id +'-base-temp').value;
    this.species[species_id].percent = $(species_id + '-percent').value;
    this.species[species_id].R0 = $(species_id + '-R0').value;
    this.species[species_id].E0 = $(species_id + '-E0').value;

    if (this.species[species_id].name !== '' &&
        this.species[species_id].basetemp !== '' &&
        this.species[species_id].R0 !== '' &&
        this.species[species_id].E0 !== '' &&
        this.species[species_id].percent !== '') {
        this.species[species_id].valid = true;
    }
};

// overrides function in graph.js
function initForestGraph() {
    clearError();
    var g = new Bluff.Bar('graph', '460x345');
    g.set_theme({
        ///note: not used since we do this in leafGraph() now.
        marker_color: '#aea9a9',
        font_color: 'black',
        background_colors: ['white', 'white']
    });
    g.hide_title = true;
    g.x_axis_label = 'Scenarios';
    g.sort = false;
    g.set_margins(10);
    g.left_margin = 25;
    g.no_data_message = 'Press \'Graph\' to graph data.';
    g.no_data_font_size = '21';
    return g;
}

/* Called onclick of the graph button */
function forestGraph() {
    // have to re-init, because g.clear() doesn't reset legend
    var g = new initForestGraph();
    var scenario_count = 0;
    var data = [];
    var scids = [];
    var headers = [['Content-Type', 'application/x-www-form-urlencoded']];
    var all_valid = true;

    forEach(getElementsByTagAndClassName('div', 'scenario'),
        function(scenario) {
            var scid = scenario.id;
            ForestData.updateScenario(scid);

            if (!ForestData.scenarios[scid].valid) {
                alert(ForestData.scenarios[scid].name +
                        ' cannot be graphed. Please enter valid ' +
                        'values for all species and advanced ' +
                        'options. Species compositions must add up ' +
                        'to 100% in a single scenario.');
                all_valid = false;
                return;
            }
        }
    );

    if (!all_valid) {
        return;
    }

    var scenarios = getElementsByTagAndClassName('div', 'scenario');
    forEach(scenarios, function(scenario) {
        var scid = scenario.id;
        if (ForestData.scenarios[scid].valid) {
            scenario_count++;
            var station = ForestData.scenarios[scid].station;
            var start = ForestData.scenarios[scid].start;
            var end = ForestData.scenarios[scid].end;
            var deltaT = ForestData.scenarios[scid].deltaT;
            var leafarea = ForestData.scenarios[scid].leafarea;
            data[scenario_count-1] = 0;
            var species_count = 0;

            var all_species =
                getElementsByTagAndClassName('div', 'species', scenario);
            forEach(all_species, function(species) {
                if (ForestData.species[species.id].valid) {
                    species_count++;
                    var base_temp = parseInt(
                        ForestData.species[species.id].basetemp, 10);
                    var basetemp = parseInt(base_temp, 10) + 273.15;
                    var R0 = ForestData.species[species.id].R0;
                    var E0 = ForestData.species[species.id].E0;
                    var percent = ForestData.species[species.id].percent;
                    var params = 'R0=' + R0 + '&E0=' + E0 + '&t0=' +
                        basetemp + '&station=' + station + '&start=' +
                        start + '&end=' + end + '&delta=' + deltaT;
                    var http_request = doXHR('getsum', {
                        'method': 'POST',
                        'sendContent': params,
                        'headers': headers
                    });

                    // eslint-disable-next-line no-inner-declarations
                    function my_callback(
                        scenario_num, scid, percent, http_request) {

                        var answer = evalJSON(http_request.responseText);
                        data[scenario_num-1] +=
                            answer.total * (percent/100.0);
                        species_count--;

                        if (species_count === 0) {
                            // got all species totals for this scenario
                            data[scenario_num-1] =
                                data[scenario_num-1] * leafarea;
                            var calculated_value =
                                Math.round(data[scenario_num-1] * 100) / 100;
                            data[scenario_num-1] = calculated_value;
                            scids[scenario_num-1] = scid;
                            scenario_count--;

                            if (scenario_count === 0) {
                                for (var i=0; i < data.length; i++) {
                                    var s = ForestData.scenarios[scids[i]];
                                    var l = s.name + ' (' + data[i]  + ')';
                                    g.data(l, data[i], s.color);
                                }

                                g.minimum_value = 0;
                                g.draw();
                            }
                        }
                    }
                    // okay... so we are telling addCallback which is an
                    // asycn req to accept a possibly partial list or
                    // arguments? why is it sending a request for EVERY
                    // species when it already has the information and
                    // can send it at once???
                    http_request.addCallback(
                        partial(my_callback, scenario_count, scid, percent));
                }
            });
        }
    });
}

function setupForest() {
    var g = initGraph();
    g.draw();
}

// overrides function in graph.js
LeafGraphData.prototype.updateFields = function() {
    return;
};

function calculateKelvin(elem, id) {
    var k = id.split('-');
    var kl = k[0] + '-kelvin';
    var result = parseFloat(elem) + 273.15;
    var kelvin = document.getElementById(kl);

    if (isNaN(result)) {
        kelvin.innerHTML = '';
    } else {
        kelvin.innerHTML = result;
    }
}

function makeExportLink(a) {
    var id = id.split('-')[0];
    var year = document.getElementById(id + '-year').value;
    var start = document.getElementById(id + '-startdate').value;
    var end = document.getElementById(id + '-enddate').value;
    var station = document.getElementById(id + '-fieldstation').value;

    a.href = '/respiration/getcsv?year=' + year + '&start=' + start +
        '&end=' + end + '&station=' + station;
}

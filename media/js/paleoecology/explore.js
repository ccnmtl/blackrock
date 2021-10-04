var visible = null;
var global_http_request;

var images = [
    [
        'Abies (Fir)', 'Alnus (Alder)', 'Asteraceae (Ragweed & herbs)',
        'Betula (Birch)', 'Carya (Hickory)',
        'Castanea dentata (American Chestnut)',
        'Cyperaceae (Sedge)', 'Fagus grandifolia (American Beech)',
        'Fraxinus (Ash)', 'Gramineae (Grasses)', 'Ostrya/Carpinus',
        'Picea (Spruce)',
        'Pinus (Pine)', 'Quercus (Oak)', 'Tsuga canadensis (Eastern Hemlock)'],
    [
        'id02.jpg', 'id03.jpg', 'id04.jpg', 'id05.jpg', 'id08.jpg', 'id09.jpg',
        'id10.jpg', 'id11.jpg', 'id12.jpg', 'id13.jpg', 'id14.jpg', 'id16.jpg',
        'id18.jpg', 'id19.jpg', 'id21.jpg']
];

//colors for pie charts (need 16 colors, 15 pollen types + 'other')
var colors = [
    'A6CEE3', '1F78B4', 'B2DF8A', '33A02C', 'FB9A99', 'E31A1C',
    'FDBF6F', 'FF7F00', 'CAB2D6', '6A3D9A', 'FFD700',
    'A0522D', '336633', '696969', 'A9A9A9', 'EBEBEB'];

function getImage(name) {
    for (var idx = 0; idx < images[0].length; idx++) {
        if (images[0][idx] === name) {
            return images[1][idx];
        }
    }
    return null;
}

function showResults(http_request) {
    global_http_request = http_request;

    var results = evalJSON(http_request.responseText);

    var depth = results.depth;
    var pollen = results.pollen;
    var counts = results.counts;
    var percents = results.percents;
    var otherPercent = results.other;

    var divCounts = $('sample-counts-' + depth);
    var divPercents = $('sample-percents-' + depth);

    // use Google charts API to create pie chart
    var baseURL = 'https://chart.googleapis.com/chart?cht=p';
    var chartSize = 'chs=' + '260x400' + '&chdlp=bv';
    var chartLabels = 'chdl=';

    var chartColors = 'chco=';

    if (pollen.length === 0) {
        divCounts.innerHTML = 'No data.';
        divPercents.innerHTML = '';

        var imgSrc = baseURL + '&chs=200x200&chco=' + colors[15] +
            '&chd=t:100&chdl=Other (100%)&chdlp=bv';

        $('sample-chart-' + depth).src = imgSrc;
        return;
    }

    var countString = '<br />';
    for (var i = 0; i < pollen.length; i++) {
        var imgString = '<div class="pollen-zoo-image core">' +
            '<div id="pollen-image-' + i + '">' +
            '<img src="' + STATIC_URL + 'images/paleoecology/pollen/' +
            getImage(pollen[i]) + '"/></div>';
        countString += imgString + '<div class="imagename"><b>' + pollen[i] +
            ':</b><br /> ' + counts[i] + ' grains <br /></div></div>';
        chartLabels += escape(pollen[i]) + ' (' + percents[i] + '%)|';
    }

    // use names instead of pollen so we keep the colors consistent over graphs
    for (var j = 0; j < images[0].length; j++) {
        var pollenName = images[0][j];
        if (pollen.join('').indexOf(pollenName) !== -1) {
            chartColors += colors[j] + ',';
        }
    }
    if (otherPercent > 0) {
        chartColors += colors[15];
    } else {
        // remove trailing comma
        chartColors = chartColors.substr(0, chartColors.length - 1);
    }

    chartLabels += 'Other (' + otherPercent + '%)';
    var chartData = 'chd=t:' + percents.join(',') + ',' + otherPercent;
    var chartSrc = baseURL + '&' + chartColors + '&' + chartSize + '&' +
        chartData + '&' + chartLabels;

    $('sample-chart-' + depth).src = chartSrc;
    divPercents.innerHTML = '';
    divCounts.innerHTML = countString;
}

function showError(http_request) {
    global_http_request = http_request;
    log(http_request);
}

function showSample(e) {
    var depth = e.src().id.substr(11);

    if (visible) {
        hideElement(visible);
    }
    visible = $('sample-info-' + depth);

    if (!visible) {
        return;
    }

    showElement(visible);

    // load data as needed
    if (hasElementClass(visible, 'unloaded')) {
        var params = 'depth=' + depth;
        global_http_request = doXHR('getpercents', {
            'method': 'POST',
            'sendContent': params,
            'headers': [['Content-Type', 'application/x-www-form-urlencoded']]
        });
        global_http_request.addCallback(showResults);
        global_http_request.addErrback(showError);
        removeElementClass(visible, 'unloaded');
    }
}

function setupCore() {
    forEach(getElementsByTagAndClassName('div', 'core-slice'), function(elem) {
        connect(elem, 'onclick', showSample);
    });
}

addLoadEvent(setupCore);

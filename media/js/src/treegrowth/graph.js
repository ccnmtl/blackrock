/* jshint esversion: 6 */
/* global Papa: true, Treegrowth: true */

(function() {
    var BASE_PATH = 'https://www1.columbia.edu/sec/ccnmtl/projects/' +
        'blackrock/forestdata/processed_data/';
    var MNT_MISERY_DATA = BASE_PATH + 'Mnt_Misery_Table20.csv';
    var WHITE_OAK_DATA = BASE_PATH + 'White_Oak_Table20.csv';
    var ENV_DATA = BASE_PATH + 'Lowland.csv';

    var initGraph = function(data) {
        var seriesOptions = [];
        var yAxes = [];
        var headers = [
            'Red_Oak_1_AVG', 'Red_Oak_2_AVG',
            'Red_Oak_3_AVG', 'Red_Oak_4_AVG',
            'Red_Oak_5_AVG',
            'Site AVG', 'Site STD DEV',
            'White_Oak_1_AVG', 'White_Oak_2_AVG',
            'White_Oak_3_AVG', 'White_Oak_4_AVG',
            'White_Oak_5_AVG',
            'Site AVG', 'Site STD DEV',
            'AvgTEMP_C', 'AvgVP', 'TotalRain',
            'SoilM_5cm', 'AvgPAR_Den'
        ];
        for (var i = 0; i < data.length; i++) {
            var name = 'Series ' + (i + 1);
            if (i < headers.length) {
                name = headers[i];
            }

            var series = {};
            var yAxis = {};
            if (name === 'Site STD DEV') {
                var stdDevData = [];
                for (var j = 0; j < data[i].length; j += 4) {
                    var group = [];
                    try {
                        group = [
                            data[i][j][0],
                            data[i][j][1],
                            data[i][j + 1][1],
                            data[i][j + 2][1],
                            data[i][j + 3][1]
                        ];
                    } catch (e) {
                        continue;
                    }

                    var values = group.slice(1);
                    var max = Math.max(...values);
                    var min = Math.min(...values);

                    var candlestick = [
                        group[0], // timestamp
                        group[1], // open
                        max,
                        min,
                        group[group.length - 1] // close
                    ];
                    stdDevData.push(candlestick);
                }
                series = {
                    type: 'candlestick',
                    name: name,
                    data: stdDevData,
                    yAxis: i,
                    dataGrouping: {
                        units: [
                            ['hour', [1, 8, 16]],
                            ['day', [1, 7]]
                        ]
                    }
                };
                yAxis = {
                    title: {
                        text: name
                    },
                    visible: false
                };
            } else {
                var isVisible = true;
                if (name.indexOf('Red_Oak_') > -1 ||
                    name.indexOf('White_Oak_') > -1
                   ) {
                    isVisible = false;
                }

                series = {
                    name: name,
                    data: data[i],
                    yAxis: i,
                    visible: isVisible
                };

                // Environmental data has units
                if (name === 'AvgTEMP_C') {
                    series.tooltip = {
                        valueSuffix: '°C'
                    };
                } else if (name === 'AvgVP') {
                    series.tooltip = {
                        valueSuffix: ' kPa'
                    };
                } else if (name === 'TotalRain') {
                    series.tooltip = {
                        valueSuffix: ' mm'
                    };
                } else if (name === 'SoilM_5cm') {
                    series.tooltip = {
                        valueSuffix: ' VWC'
                    };
                } else if (name === 'AvgPAR_Den') {
                    series.tooltip = {
                        valueSuffix: ' umol/s/m²'
                    };
                }

                yAxis = {
                    title: {
                        text: name
                    },
                    visible: false
                };
            }

            seriesOptions.push(series);
            yAxes.push(yAxis);
        }
        $('#plot-container').highcharts('StockChart', {
            rangeSelector: {
                selected: 1
            },
            navigator: {
                series: {
                    includeInCSVExport: false
                }
            },
            legend: {
                enabled: true,
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            yAxis: yAxes,
            series: seriesOptions
        });
    };

    var downloadAndParse = function($promise, path) {
        var timestamp = (new Date()).getTime();
        Papa.parse(path + '?' + timestamp, {
            dynamicTyping: true,
            skipEmptyLines: true,
            download: true,
            complete: function(results, file) {
                var data = results.data;

                // Remove header row
                data.shift();

                data = Treegrowth.convertToMilliseconds(data);

                $promise.resolve(Treegrowth.splitData(data));
            },
            error: function(e) {
                $promise.reject(e);
            }
        });
    };

    /**
     * Takes the paths of the dendrometer and environmental CSV files,
     * downloads and parses these files, and initiates the graph.
     */
    var getData = function(mntMiseryPath, whiteOakPath, environmentalPath) {
        var timestamp = (new Date()).getTime();

        var $dfd1 = $.Deferred();
        downloadAndParse($dfd1, mntMiseryPath);

        var $dfd2 = $.Deferred();
        downloadAndParse($dfd2, whiteOakPath);

        var $dfd3 = $.Deferred();
        downloadAndParse($dfd3, environmentalPath);

        var promises = [$dfd1, $dfd2, $dfd3];
        $.when.apply(this, promises).then(function(d1, d2, d3) {
            $(document).ready(function() {
                initGraph(d1.concat(d2).concat(d3));
            });
        });
    };

    getData(MNT_MISERY_DATA, WHITE_OAK_DATA, ENV_DATA);
})();

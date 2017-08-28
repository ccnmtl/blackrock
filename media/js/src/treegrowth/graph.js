/* jshint esversion: 6 */
/* global Papa: true, Treegrowth: true */

(function() {
    var BASE_PATH = 'https://www1.columbia.edu/sec/ccnmtl/projects/' +
        'blackrock/forestdata/processed_data/';
    var MNT_MISERY_DATA = BASE_PATH + 'Mnt_Misery_Table20.csv';
    var WHITE_OAK_DATA = BASE_PATH + 'White_Oak_Table20.csv';
    var ENV_DATA = BASE_PATH + 'Lowland.csv';
    var MAILLEYS_MILL_DATA = BASE_PATH + 'Mailley\'s_Mill_Table20Min.csv';

    var initMainGraph = function(data) {
        var seriesOptions = [];
        var yAxes = [];
        var headers = [
            'Red_Oak_1_AVG', 'Red_Oak_2_AVG',
            'Red_Oak_3_AVG', 'Red_Oak_4_AVG',
            'Red_Oak_5_AVG',
            'Site AVG',
            'White_Oak_1_AVG', 'White_Oak_2_AVG',
            'White_Oak_3_AVG', 'White_Oak_4_AVG',
            'White_Oak_5_AVG',
            'Site AVG',
            'AvgTEMP_C', 'AvgVP', 'TotalRain',
            'SoilM_5cm', 'AvgPAR_Den'
        ];
        var newHeaderNames = [
            'S1 Oak 1', 'S1 Oak 2',
            'S1 Oak 3', 'S1 Oak 4',
            'S1 Oak 5',
            'Site 1 AVG',
            'S2 Oak 1', 'S2 Oak 2',
            'S2 Oak 3', 'S2 Oak 4',
            'S2 Oak 5',
            'Site 2 AVG',
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

            var isVisible = true;
            if (name.indexOf('Red_Oak_') > -1 ||
                name.indexOf('White_Oak_') > -1
               ) {
                isVisible = false;
            }

            var showInNavigator = false;
            if (i === 5) {
                showInNavigator = true;
            }

            series = {
                showInNavigator: showInNavigator,
                name: newHeaderNames[i],
                data: data[i],
                visible: isVisible
            };

            // Don't use separate y-axes for the trees that we're
            // calculating an absolute RDH (radius at dendrometer
            // height) for. And add units.
            if (newHeaderNames[i].match(/^S\d Oak \d$/)) {
                series.tooltip = {
                    valueSuffix: ' deltaRDH (μm)'
                };
            } else {
                series.yAxis = i;
            }

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
                visible: false
            };

            var pointFormatter = function() {
                var unit = '';
                if (this.series.options.tooltip.valueSuffix) {
                    unit = this.series.options.tooltip.valueSuffix;
                }
                var val = +this.y.toFixed(3);
                return '<span style="color:{' + this.color + '}">' +
                    '\u25CF</span> ' + this.series.name + ': ' +
                    '<strong>' + val + ' ' + unit +
                    '</strong>' +
                    '<br/>';
            };
            if (!series.tooltip) {
                series.tooltip = {};
            }
            series.tooltip.pointFormatter = pointFormatter;

            seriesOptions.push(series);
            yAxes.push(yAxis);
        }
        $('#plot-container').highcharts('StockChart', {
            chart: {
                height: 440
            },
            colors: [
                // Site 1
                '#FF8A80', '#EA80FC', '#FF1744', '#D500F9', '#C51162',
                '#E91E63',
                // Site 2
                '#80D8FF', '#A7FFEB', '#00B0FF', '#1DE9B6', '#00B8D4',
                '#00BCD4',
                // Environmental data
                '#FF9800', '#FDD835', '#3D5AFE', '#795548', '#757575'
            ],
            rangeSelector: {
                selected: 0,
                buttons: [{
                    type: 'week',
                    count: 1,
                    text: '1w'
                }, {
                    type: 'month',
                    count: 1,
                    text: '1m'
                }, {
                    type: 'month',
                    count: 3,
                    text: '3m'
                }, {
                    type: 'ytd',
                    text: 'YTD'
                }, {
                    type: 'all',
                    text: 'All'
                }]
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
                borderWidth: 0,
                title: {
                    text: 'Black Rock Forest'
                },
                labelFormatter: function() {
                    if (this.name.match(/S\d Oak/)) {
                        return '<div style="margin-left: 14px;">' +
                            this.name + '</div>';
                    }
                    return '<div>' + this.name + '</div>';
                },
                useHTML: true
            },
            scrollbar: {
                enabled: false
            },
            xAxis: {
                dateTimeLabelFormats: {
                    day: '%e %b',
                    week: '%e %b'
                }
            },
            yAxis: yAxes,
            series: seriesOptions,
            exporting: {
                sourceWidth: 1024,
                sourceHeight: 768,
                buttons: {
                    customButton: {
                        y: 36,
                        align: 'right',
                        text: 'Reset selections',
                        theme: {
                            stroke: '#cccccc'
                        },
                        onclick: function() {
                            initMainGraph(data);
                        }
                    }
                }
            },
            plotOptions: {
                line: {
                    dataGrouping: {
                        enabled: false
                    }
                }
            }
        });
    };

    var initMailleysMillGraph = function(data) {
        var seriesOptions = [];
        var yAxes = [];
        var newHeaderNames = [
            'Hemlock 1', 'Hemlock 2', 'Hemlock 3',
            'Pine 1', 'Pine 2', 'Pine 3', 'Site AVG',
            'AvgTEMP_C', 'AvgVP', 'TotalRain',
            'SoilM_5cm', 'AvgPAR_Den'
        ];

        for (var i = 0; i < data.length; i++) {
            var series = {};
            var yAxis = {};

            series = {
                name: newHeaderNames[i],
                data: data[i],
                yAxis: i
            };

            yAxis = {
                visible: false
            };

            var pointFormatter = function() {
                var unit = '';
                if (this.series.options.tooltip.valueSuffix) {
                    unit = this.series.options.tooltip.valueSuffix;
                }
                var val = +this.y.toFixed(3);
                return '<span style="color:{' + this.color + '}">' +
                    '\u25CF</span> ' + this.series.name + ': ' +
                    '<strong>' + val + ' ' + unit +
                    '</strong>' +
                    '<br/>';
            };
            if (!series.tooltip) {
                series.tooltip = {};
            }
            series.tooltip.pointFormatter = pointFormatter;

            seriesOptions.push(series);
            yAxes.push(yAxis);
        }
        $('#mailleys-mill-plot-container').highcharts('StockChart', {
            chart: {
                height: 440
            },
            rangeSelector: {
                selected: 0,
                buttons: [{
                    type: 'week',
                    count: 1,
                    text: '1w'
                }, {
                    type: 'month',
                    count: 1,
                    text: '1m'
                }, {
                    type: 'month',
                    count: 3,
                    text: '3m'
                }, {
                    type: 'ytd',
                    text: 'YTD'
                }, {
                    type: 'all',
                    text: 'All'
                }]
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
                borderWidth: 0,
                title: {
                    text: 'Mailley\'s Mill'
                },
                labelFormatter: function() {
                    if (this.name.match(/S\d Oak/)) {
                        return '<div style="margin-left: 14px;">' +
                            this.name + '</div>';
                    }
                    return '<div>' + this.name + '</div>';
                },
                useHTML: true
            },
            scrollbar: {
                enabled: false
            },
            xAxis: {
                dateTimeLabelFormats: {
                    day: '%e %b',
                    week: '%e %b'
                }
            },
            yAxis: yAxes,
            series: seriesOptions,
            exporting: {
                sourceWidth: 1024,
                sourceHeight: 768,
                buttons: {
                    customButton: {
                        y: 36,
                        align: 'right',
                        text: 'Reset selections',
                        theme: {
                            stroke: '#cccccc'
                        },
                        onclick: function() {
                            initMailleysMillGraph(data);
                        }
                    }
                }
            },
            plotOptions: {
                line: {
                    dataGrouping: {
                        enabled: false
                    }
                }
            }
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
    var getData = function(
        mntMiseryPath, whiteOakPath, environmentalPath, mailleysMillData
    ) {
        var $dfd1 = $.Deferred();
        downloadAndParse($dfd1, mntMiseryPath);

        var $dfd2 = $.Deferred();
        downloadAndParse($dfd2, whiteOakPath);

        var $dfd3 = $.Deferred();
        downloadAndParse($dfd3, environmentalPath);

        var promises = [$dfd1, $dfd2, $dfd3];
        $.when.apply(this, promises).then(function(d1, d2, d3) {
            $(document).ready(function() {
                initMainGraph(d1.concat(d2).concat(d3));
            });
        });

        var $dfd4 = $.Deferred();
        downloadAndParse($dfd4, mailleysMillData);

        var promises2 = [$dfd4, $dfd3];
        $.when.apply(this, promises2).then(function(d1, d2) {
            $(document).ready(function() {
                initMailleysMillGraph(d1.concat(d2));
            });
        });
    };

    getData(MNT_MISERY_DATA, WHITE_OAK_DATA, ENV_DATA, MAILLEYS_MILL_DATA);
})();

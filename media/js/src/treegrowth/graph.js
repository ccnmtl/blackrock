/* jshint esversion: 6 */
/* global Papa: true, Treegrowth: true */

(function() {
    var DENDROMETER_PATH = 'https://www1.columbia.edu/sec/ccnmtl/projects/' +
        'blackrock/forestdata/processed_data/Mnt_Misery_Table20.csv';
    var ENVIRONMENTAL_PATH = 'https://www1.columbia.edu/sec/ccnmtl/projects/' +
        'blackrock/forestdata/processed_data/Lowland.csv';

    var initGraph = function(data) {
        var seriesOptions = [];
        var yAxes = [];
        var headers = [
            'Red_Oak_1_AVG', 'Red_Oak_2_AVG',
            'Red_Oak_3_AVG', 'Red_Oak_4_AVG',
            'Red_Oak_5_AVG',
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
                    top: '65%',
                    height: '35%',
                    visible: false
                };
            } else {
                series = {
                    name: name,
                    data: data[i],
                    yAxis: i
                };
                yAxis = {
                    title: {
                        text: name
                    },
                    height: '65%',
                    visible: false
                };
            }

            seriesOptions.push(series);
            yAxes.push(yAxis);
        }
        $('#plot-container').highcharts('StockChart', {
            chart: {
                height: 600
            },
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

    /**
     * Takes the paths of the dendrometer and environmental CSV files,
     * downloads and parses these files, and initiates the graph.
     */
    var getData = function(dendrometerPath, environmentalPath) {
        var timestamp = (new Date()).getTime();

        var $dendDfd = $.Deferred();
        Papa.parse(dendrometerPath + '?' + timestamp, {
            dynamicTyping: true,
            skipEmptyLines: true,
            download: true,
            //header: true,
            complete: function(results, file) {
                var data = results.data;

                // Remove header row
                data.shift();

                data = Treegrowth.convertToUnixTimestamps(data);

                $dendDfd.resolve(Treegrowth.splitData(data));
            },
            error: function(e) {
                $dendDfd.reject(e);
            }
        });

        var $envDfd = $.Deferred();
        Papa.parse(environmentalPath + '?' + timestamp, {
            dynamicTyping: true,
            skipEmptyLines: true,
            download: true,
            complete: function(results, file) {
                var data = results.data;

                // Remove header row
                data.shift();

                data = Treegrowth.convertToUnixTimestamps(data);

                $envDfd.resolve(Treegrowth.splitData(data));
            },
            error: function(e) {
                $envDfd.reject(e);
            }
        });

        var promises = [$dendDfd, $envDfd];
        $.when.apply(this, promises).then(function(dData, eData) {
            $(document).ready(function() {
                initGraph(dData.concat(eData));
            });
        });
    };

    getData(DENDROMETER_PATH, ENVIRONMENTAL_PATH);
})();

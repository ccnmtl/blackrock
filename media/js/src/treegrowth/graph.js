/* global Papa: true, console: true */

(function() {
    var DENDROMETER_PATH = 'https://www1.columbia.edu/sec/ccnmtl/projects/' +
        'blackrock/forestdata/processed_data/Mnt_Misery_Table20.csv';
    var ENVIRONMENTAL_PATH = 'https://www1.columbia.edu/sec/ccnmtl/projects/' +
        'blackrock/forestdata/processed_data/Lowland.csv';

    /**
     * Given a 2-dimensional array representation of CSV data,
     * split it out into something Highstock can understand. For
     * example:
     *
     * input: [
     *    [ 100, 2, 4 ],
     *    [ 101, 3, 1 ],
     *    [ 102, 6, 2 ],
     *    [ 103, 9, 3 ]
     * ]
     *
     * output: [
     *     [
     *         [ 100, 2 ],
     *         [ 101, 3 ],
     *         [ 102, 6 ],
     *         [ 103, 9 ]
     *     ],
     *     [
     *         [ 100, 4 ],
     *         [ 101, 1 ],
     *         [ 102, 2 ],
     *         [ 103, 3 ]
     *     ]
     * ]
     *
     *
     */
    var splitData = function(data) {
        var newData = [];
        for (var i = 0; i < data.length; i++) {
            for (var j = 1; j < data[i].length; j++) {
                if (i === 0) {
                    newData.push([]);
                }
                if (!newData[j - 1]) {
                    console.error('splitData error:', newData);
                    continue;
                }
                newData[j - 1].push([
                    data[i][0], data[i][j]
                ]);
            }
        }
        return newData;
    };

    var parseDate = function(s) {
        var b = s.split(/\D+/);
        return new Date(b[0], parseInt(b[1]) - 1, b[2], b[3], b[4], b[5]);
    };

    /**
     * Convert the first column of each row to its unix timestamp.
     */
    var convertToUnixTimestamps = function(data) {
        for (var i = 0; i < data.length; i++) {
            var date = Date.parse(data[i][0]);
            if (isNaN(date)) {
                // Safari has trouble parsing the date!
                date = parseDate(data[i][0]);
            }
            data[i][0] = date;
        }
        return data;
    };

    var initGraph = function(data) {
        var seriesOptions = [];
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
            seriesOptions.push({
                name: name,
                data: data[i]
            });
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

                data = convertToUnixTimestamps(data);

                $dendDfd.resolve(splitData(data));
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

                data = convertToUnixTimestamps(data);

                $envDfd.resolve(splitData(data));
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

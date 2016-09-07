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
            seriesOptions.push({
                name: name,
                data: data[i],
                yAxis: i
            });
            yAxes.push({
                title: {
                    text: name
                },
                visible: false
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

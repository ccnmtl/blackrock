/* global Papa: true */

(function() {
    var DENDROMETER_PATH = 'https://www1.columbia.edu/sec/ccnmtl/projects/' +
        'blackrock/forestdata/processed_data/Mnt_Misery_Table20.csv';
    var ENVIRONMENTAL_PATH = 'https://www1.columbia.edu/sec/ccnmtl/projects/' +
        'blackrock/forestdata/data/current/Lowland.csv';

    var initGraph = function(data) {
        $('#plot-container').highcharts('StockChart', {
            rangeSelector: {
                selected: 1
            },
            navigator: {
                series: {
                    includeInCSVExport: false
                }
            },
            data: {
                rows: data
            },
            legend: {
                enabled: true,
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            }
        });
    };

    /**
     * Takes the paths of the dendrometer and environmental CSV files,
     * downloads and parses these files, and initiates the graph.
     */
    var getData = function(dendrometerPath, environmentalPath) {
        var $dendDfd = $.Deferred();
        Papa.parse(dendrometerPath, {
            download: true,
            complete: function(results, file) {
                var data = results.data;
                data.pop();
                $dendDfd.resolve(data);
            },
            error: function(e) {
                $dendDfd.reject(e);
            }
        });

        var $envDfd = $.Deferred();
        Papa.parse(environmentalPath, {
            download: true,
            complete: function(results, file) {
                var data = results.data;
                data.pop();
                $envDfd.resolve(data);
            },
            error: function(e) {
                $envDfd.reject(e);
            }
        });

        var promises = [$dendDfd];
        $.when.apply(this, promises).then(function(dData, eData) {
            $(document).ready(function() {
                initGraph(dData);
            });
        });
    };

    getData(DENDROMETER_PATH, ENVIRONMENTAL_PATH);
})();

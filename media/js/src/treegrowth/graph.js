/* global Papa: true */

(function() {
    var BASE_URL = 'https://www1.columbia.edu/sec/ccnmtl/projects/' +
        'blackrock/forestdata/data/current/';
    var FILENAME = 'Mnt_Misery_Table20.csv';

    var initChart = function(data) {
        $('#plot-container').highcharts('StockChart', {
            rangeSelector: {
                selected: 1
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

    Papa.parse(BASE_URL + FILENAME, {
        download: true,
        complete: function(results, file) {
            var data = results.data;

            // Remove unnecessary rows from CSV.
            data.shift();
            data.splice(1, 2);
            data.pop();

            $(document).ready(function() {
                initChart(data);
            });
        }
    });
})();

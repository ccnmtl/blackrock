/* global Papa: true */

(function() {
    // Fetching from cunix requires CORS
    // var CUNIX_BASE = 'https://www1.columbia.edu/sec/ccnmtl/projects/' +
    //    'blackrock/forestdata/data/current/';

    var FILENAME = 'Mnt_Misery_Hourly.csv';

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

    Papa.parse('/media/uploads/' + FILENAME, {
        download: true,
        complete: function(results, file) {
            var data = results.data;
            data.pop();

            $(document).ready(function() {
                initChart(data);
            });
        }
    });
})();

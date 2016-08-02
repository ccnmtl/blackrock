/* global Papa: true */

(function() {
    var BASE_URL = 'https://www1.columbia.edu/sec/ccnmtl/projects/' +
        'blackrock/forestdata/processed_data/';
    var FILENAME = 'Mnt_Misery_Table20.csv';

    var initChart = function(data) {
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

    Papa.parse(BASE_URL + FILENAME, {
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

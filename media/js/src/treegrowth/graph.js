/* global Papa: true */

(function() {
    var BASE_URL =
        'https://s3.amazonaws.com/ccnmtl-blackrock-static-prod/media/';
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
            data.pop();

            $(document).ready(function() {
                initChart(data);
            });
        }
    });
})();

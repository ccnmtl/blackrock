(function() {
    // Fetching from cunix requires CORS
    // var CUNIX_BASE = 'https://www1.columbia.edu/sec/ccnmtl/projects/' +
    //    'blackrock/forestdata/data/current/';

    var FILENAME = 'Mnt_Misery_Hourly.csv';

    var initChart = function(data) {
        $('#plot-container').highcharts({
            title: {
                text: 'Dendrometer Data'
            },
            data: {
                csv: data
            },
            chart: {
                zoomType: 'x'
            },
            plotOptions: {
                series: {
                    marker: {
                        enabled: false
                    }
                }
            },
            series: [{
                lineWidth: 1
            }, {
                type: 'line',
                color: '#c4392d',
                negativeColor: '#5679c4',
                fillOpacity: 0.5
            }]
        });
    };

    $(document).ready(function() {
        $.ajax({
            type: 'GET',
            url: '/media/uploads/' + FILENAME,
            dataType: 'text',
            success: function(data) {
                initChart(data);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                alert('Status: ' + xhr.status + '    Error: ' + thrownError);
            }
        });
    });
})();

/* global console: true, exports: true */

if (typeof Treegrowth === 'undefined') {
    var Treegrowth = {};
}

(function() {
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
        if (s === null) {
            s = '';
        }
        var b = s.split(/\D+/);
        var date = Date.UTC(b[0], parseInt(b[1]) - 1, b[2], b[3], b[4], b[5]);
        return date;
    };

    /**
     * Convert the first column of each row to an integer timestamp.
     */
    var convertToMilliseconds = function(data) {
        for (var i = 0; i < data.length; i++) {
            var date = parseDate(data[i][0]);
            data[i][0] = date;
        }
        return data;
    };

    /**
     * Returns the CSV data with the given column indices removed.
     */
    var removeColumns = function(data, indices) {
        indices.sort(function(a, b) {
            return a - b;
        });
        indices.reverse();

        indices.forEach(function(x) {
            data.splice(x, 1);
        });
    };

    var removeHeaderRows = function(data) {
        data.forEach(function(column) {
            column.shift();
            column.shift();
            column.shift();
        });
    };

    Treegrowth.splitData = splitData;
    Treegrowth.parseDate = parseDate;
    Treegrowth.convertToMilliseconds = convertToMilliseconds;
    Treegrowth.removeColumns = removeColumns;
    Treegrowth.removeHeaderRows = removeHeaderRows;
})();

if (typeof exports !== 'undefined') {
    exports.Treegrowth = Treegrowth;
}

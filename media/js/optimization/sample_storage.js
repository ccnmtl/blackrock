/* global Stor: true */
/* exported SampleStorage */

// eslint-disable-next-line no-unused-vars
var SampleStorage = (new (
    function() {
        if (!window.JSON || !window.Stor) {
            throw Error('we need a modern browser to store stuff');
        }
        var self = this;
        this.nsINDEX = 'ALL_SAMPLES';
        this.nsSAMPLE = 'SAMPLE_';
        this.nsFOREST = 'FOREST'; //summary forest 'actual' data

        this.addSample = function(summary, results) {
            var index = self.samples.push(summary) -1;
            Stor.set(self.nsSAMPLE + index, JSON.stringify(results));
            Stor.set(self.nsINDEX, JSON.stringify(self.samples));
            return index;
        };

        this.getSample = function(index) {
            return JSON.parse(Stor.get(self.nsSAMPLE + index,'false'));
        };
        this.getSampleRaw = function(index) {
            return Stor.get(self.nsSAMPLE + index,'');
        };

        this.deleteSample = function(index) {
            Stor.del(self.nsSAMPLE + index);
            self.samples[index] = false;
            Stor.set(self.nsINDEX, JSON.stringify(self.samples));
        };

        this.setForest = function(results) {
            var summary = [
                'FOREST',
                0,0,0,0,
                results['actual-area'],
                0,0,0,0,
                results['actual-species'],
                results['actual-count'],
                results['actual-dbh'],
                results['actual-variance-dbh'],
                results['actual-density'],
                results['actual-basal']
            ];
            Stor.set(self.nsFOREST, JSON.stringify(summary));
        };

        this.getForest = function() {
            return JSON.parse(Stor.get(self.nsFOREST,'[]'));
        };

        this.samples = JSON.parse(Stor.get(this.nsINDEX,'[]'));
    })());

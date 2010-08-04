var SampleStorage = (new (
function () {
    if (!window.JSON || !window.Stor) {
        throw Error("we need a modern browser to store stuff");
    }
    var self = this;
    this.nsINDEX = 'ALL_SAMPLES';
    this.nsSAMPLE = 'SAMPLE_';
    
    this.addSample = function(results) {
        var summary = [
                       results['input']['num_plots'],
                       results['input']['shape'],
                       results['input']['size'],
                       results['input']['arrangement'],
                       results['sample-time'],
                       results['avg-time'],
                       results['sample-variance-density'],
                       results['sample-variance-basal'],
                       ];
        var index = self.samples.push(summary) -1;
        Stor.set(self.nsSAMPLE + index, JSON.stringify(results));
        Stor.set(self.nsINDEX, JSON.stringify(self.samples));
        return index;
    }

    this.getSample = function(index) {
        return JSON.parse(Stor.get(self.nsSAMPLE + index,'false'));
    }
    

    this.samples = JSON.parse(Stor.get(this.nsINDEX,'[]'));
})());
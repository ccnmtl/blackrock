/* exported SampleMap */

addLoadEvent(function(){
    var map_destination = $('results-map-container');
    ///preload the image
    if (map_destination != null) {
        map_destination.appendChild(IMG({
            id: 'results-map-bg',src: 'trees.png',style: 'display:none;'}));
    }
});

// eslint-disable-next-line no-unused-vars
function SampleMap(options) {
    var self = this;
    this.init = function() {
        if (options.id) {
            $(options.id).innerHTML = '';
            options.image = options.image || $('results-map-bg');
            self.createMap(options);
        }
    };

    this.addPlot = function(plot, plotname) {
        if (plot.coordinates) {
            var feature = self.GeoJSON.parseFeature(
                {'geometry': {'type': 'Polygon',
                    'coordinates': [plot.coordinates]
                }});
            feature.plotname = plotname;
            feature.plot = plot;
            this.vectors.addFeatures([ feature ]);
        }
    };

    this.createMap = function(options) {
        var map = new OpenLayers.Map(options.id);
        var projection = 'Flatland:1'; //'EPSG:4326';
        var opt = {
            projection: projection,
            numZoomLevels: 9,
            tileSize: new OpenLayers.Size(
                options.image.width, options.image.height)
        };
        var b = options.bounds;
        //"bounds": {"right": -73.725, "bottom": 41.165, "top": 41.39,
        // "height": 0.225, "width": 0.3, "left": -74.025}
        var graphic = new OpenLayers.Layer.Image(
            'Trees in Sample Area',
            options.image.src,
            //new OpenLayers.Bounds(-180, -90, 180, 90),
            new OpenLayers.Bounds(b.left,b.bottom,b.right,b.top),
            new OpenLayers.Size(
                options.image.width, options.image.height),
            opt
        );
        var vectors = new OpenLayers.Layer.Vector(
            'Plots',
            {projection: projection});

        if (options.onHover) {
            var hover = new OpenLayers.Control.SelectFeature(vectors, {
                hover: true,
                highlightOnly: true,
                renderIntent: 'temporary',
                eventListeners: {
                    featurehighlighted: options.onHover
                }
            });
            map.addControl(hover);
            hover.activate();
        }
        if (options.onSelect) {
            var select = new OpenLayers.Control.SelectFeature(vectors, {
                clickout: true,
                eventListeners: {
                    featurehighlighted: options.onSelect
                }
            });
            map.addControl(select);
            select.activate();
        }
        map.addControl(new OpenLayers.Control.MousePosition());

        map.addLayers([graphic, vectors]);

        this.map = map;
        this.vectors = vectors;
        this.GeoJSON = new OpenLayers.Format.GeoJSON({
            'internalProjection': map.baseLayer.projection,
            'externalProjection': new OpenLayers.Projection(projection)
        });
        map.zoomToMaxExtent();

    };//end SampleMap.createMap()

    this.init();
}//end SampleMap


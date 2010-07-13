addLoadEvent(function(){
    var map_destination = $('results-map-container');
    ///preload the image
    if (map_destination != null) {
	map_destination.appendChild(IMG({id:'results-map-bg',src:'trees.png',style:'display:none;'}));
    }
});

function SampleMap(options) {
    var self = this;
    this.init = function() {
	if (options.id) {
	    $(options.id).innerHTML = '';
	    options.image = options.image || $('results-map-bg');
	    self.createMap(options);
	}
    }

    this.addPlot = function(plot, plotname) {
	if (plot.coordinates) {
	    var feature = self.GeoJSON.parseFeature(
		{'geometry':{'type':'Polygon',
			     'coordinates':[plot.coordinates]
			    }});
	    feature.plotname = plotname;
	    feature.plot = plot;
	    this.vectors.addFeatures( [ feature ]);
	}
    }

    this.createMap = function(options) {
       try {
           var map = new OpenLayers.Map(options.id);
	   var projection = 'Flatland:1'; //'EPSG:4326';
           var opt = {
	       projection:projection,
	       numZoomLevels: 9,
	       tileSize:new OpenLayers.Size(options.image.width, options.image.height)
	   };
	   var b = options.bounds;
	   //"bounds": {"right": -73.725, "bottom": 41.165, "top": 41.39, "height": 0.225, "width": 0.3, "left": -74.025}
           var graphic = new OpenLayers.Layer.Image(
                'Trees in Sample Area',
                options.image.src,
                //new OpenLayers.Bounds(-180, -90, 180, 90),
		new OpenLayers.Bounds(b.left,b.bottom,b.right,b.top),
                new OpenLayers.Size(options.image.width, options.image.height),
                opt
           );
	   var vectors = new OpenLayers.Layer.Vector(
	       "Plots",
	       {projection:projection});         
    
           var select = new OpenLayers.Control.SelectFeature(vectors, {
               //hover: true,
               onSelect: function(feature){
		   console.log(feature.plotname);
		   console.log(feature);
		   console.log(feature.geometry.getCentroid());
		   console.log(feature.plot);
	       }
           });


           map.addControl(select);
           select.activate();
	   
	   map.addControl(new OpenLayers.Control.MousePosition());
	   
           map.addLayers([graphic, vectors]);

	   this.map = map;
	   this.vectors = vectors;
	   this.GeoJSON = new OpenLayers.Format.GeoJSON(
		    {'internalProjection': map.baseLayer.projection,
		     'externalProjection': new OpenLayers.Projection(projection)}
		);
           map.zoomToMaxExtent();


       } catch(e) {
	   for (a in e) {
	       console.log(a+': '+e[a]);
	   }
       }
    
    }//end SampleMap.createMap()

    this.init();
}//end SampleMap



SampleMap.prototype.BADcreateMap = function(options) {
    var map = new OpenLayers.Map(options.id);
    var b = options.bounds;
    //this.bounds = new OpenLayers.Bounds(-180, -90, 180, 90);
    this.bounds = new OpenLayers.Bounds(b.left,b.bottom,b.right,b.top);
    console.log(this.bounds);
    var objopt = {
	numZoomLevels:3
	/*,
	sphericalMercator:false,
	projection:'Flatland:1',//'EPSG:4326',
	maxExtent:this.bounds,
	tileSize:new OpenLayers.Size(534,405)
*/
    };
    if (options.image) {
	this.graphic = new OpenLayers.Layer.Image(
	    'Trees in Sample Area',
	    options.image,
	    this.bounds.clone(),
	    new OpenLayers.Size(534,405),
	    objopt
	);
    }
    this.vectors = new OpenLayers.Layer.Vector("Plots",
					       {projection:objopt.projection});
    map.addLayers([this.graphic, this.vectors]);

    try {
	var x = this.bounds.clone();
	console.log(x.getCenterLonLat());
	console.log(map.getMaxExtent());
	console.log(map.getZoom());
	console.log(map.tileSize);
	this.map.zoomToExtent(this.bounds);
	//this.map.setCenter(this.bounds.getCenterLonLat(), this.map.getZoom());
    } catch(e) {
	for (a in e) {
	    console.log(a+': '+e[a]);
	}
    }
    this.map = map;
    return this.map;
}


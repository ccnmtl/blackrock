

function is_sandbox() {
    // this is just a placeholder, ok? don't sue me.
    return (location.href.match(/sandbox/) != null)
}


function back_to_grid_from_square () {
    if (is_sandbox()) {
         jQuery('#block_form')[0].action =   '/mammals/sandbox/grid/';
    } else {
         jQuery('#block_form')[0].action =   '/mammals/grid/';
    }
     jQuery('#block_form')[0].submit();
}


function you_are_here (location , mapInstance) {
    marker = new google.maps.Marker({ 
        position: location,
        map: mapInstance
    });
}

function trimpoint (point) {
    return [point[0].toPrecision(6),point[1].toPrecision(6)];
}

function bounds (box) {
    var bl  = lat_lng_from_point(box[0]);
    var tl  = lat_lng_from_point(box[1]);
    var tr  = lat_lng_from_point(box[2]);
    var br  = lat_lng_from_point(box[3]);
    return [ bl, tl, tr, br];
}

function make_grid_rectangle (_paths, mapInstance) {
    rect = new google.maps.Polygon ({
        paths           : _paths,
        fillOpacity     : 0.1,
        fillColor       : 'blue',
        strokeOpacity   : 0.3,
        strokeColor     : 'green',
        strokeWeight    : 1,
        map             : mapInstance
    });
    return rect;
}

function you_are_here (location , mapInstance) {
    marker = new google.maps.Marker({ 
        position: location,
        map: mapInstance
    });
}


function lat_lng_from_point(point ) {
    return new google.maps.LatLng(point[0] , point[1]);
}

function amarker (point, map) {
    marker = new google.maps.Marker({ 
        position: lat_lng_from_point(point),
        map: map
    });
}

function markers (points, map) {
    for (var i = 0; i < points.length; i++) {
       amarker (points [i], map);
    }
}

function user_location (mapInstance) {
    var position = false;
    if (typeof(google.loader) != 'undefined' && typeof(google.loader.ClientLocation) != 'undefined') {
        var lat = google.loader.ClientLocation.latitude;
        var lng = google.loader.ClientLocation.longitude;
        if (!isNaN (lat) && !isNaN (lng)) {
            you_are_here (new google.maps.LatLng(lat, lng), mapInstance);
        }
    }
    if (typeof(navigator.geolocation) != 'undefined') {
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude;
            var lng = position.coords.longitude;
            you_are_here (new google.maps.LatLng(lat, lng), mapInstance);
        });
    }
    return position;
}


function lat_lng_from_point(point ) {
    return new google.maps.LatLng(point[0] , point[1]);
}


function addTrails (mapObj) {
    var self = mapObj;
    
    var trails_kmllayer = new Portal.Layer("trails", "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/trails.kml", true);
    self.layers["trails"] = trails_kmllayer;
    trails_kmllayer.instance.setMap(self.mapInstance);
    
    var roads_kmllayer = new Portal.Layer("roads", "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/roads.kml", true);
    self.layers["roads"] = roads_kmllayer;
    roads_kmllayer.instance.setMap(self.mapInstance);
    
    
}



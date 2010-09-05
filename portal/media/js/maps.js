var map = null;
var infowindow = null;
var asset2Callout = {};

function showInfoWindow(asset_id) {
    log("AssetId: " + asset_id);
    var callout = asset2Callout[asset_id];
    log("Asset Callout Info: " + asset2Callout[asset_id]);
    var latlng = new google.maps.LatLng(callout['latitude'], callout['longitude']);
    
    if (infowindow)
        infowindow.close()
    
    var offset = new google.maps.Size(0,-30);

    infowindow = new google.maps.InfoWindow({content: callout['content'], position: latlng, pixelOffset: offset});
    infowindow.open(map);
}


function addMarker(asset_identifier, description, lat, lng) {
    var marker = null;
    if (lat && lng) {
        var latlng = new google.maps.LatLng(lat, lng);
        
        var marker = new google.maps.Marker({
            position: latlng, 
            map: map, 
            title: name
        }); 
        
        asset2Callout[asset_identifier] = { "content": description, "latitude": lat, "longitude": lng };
        log(asset_identifier + ": " + asset2Callout[asset_identifier]);
        
        google.maps.event.addListener(marker, 'click', function() {
            showInfoWindow(asset_identifier);
          });
        
        return 1;
    } else {
        return 0;
    }
}

function initializeMap() {
    
    if (!document.getElementById("map_canvas")) {
        return;
    }
   
    // Center on center of Black Rock Forest
    var latlng = new google.maps.LatLng(41.40744, -74.01457);
    var myOptions = {
        zoom: 13,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.HYBRID
        };
    
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
    
    // iterate over locations within the page, and add the requested markers
    // locations are identified as <div class="geocode"
    elements = getElementsByTagAndClassName(null, "geocode")
    forEach(elements,
            function(elem)
            {
                var asset_identifier = getFirstElementByTagAndClassName(null, "asset_identifier", elem).value;
                var description = document.getElementById(asset_identifier + "-description").innerHTML;
                var latitude = document.getElementById(asset_identifier + "-latitude").value;
                var longitude = document.getElementById(asset_identifier + "-longitude").value;
                
                addMarker(asset_identifier, description, latitude, longitude);
            });
}

google.maps.event.addDomListener(window, 'load', initializeMap);


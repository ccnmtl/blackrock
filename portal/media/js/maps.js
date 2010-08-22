var infowindow;
var map;

function addMarker(lat, lng, map, name, type, description, id, panto) {
    marker = null;
    if (lat && lng) {
        var latlng = new google.maps.LatLng(lat, lng);
        
        var marker = new google.maps.Marker({
            position: latlng, 
            map: map, 
            title: name
        });   

        var contentString = '<div style="font-size: 65%"><b>' + name + '</b><br />' +
            '<div style="color: #c6c6c6; padding-bottom: 5px;">' + type + '<br /></div>' +
            '<div style="font-size: 65%">' + description + ' ' + 
            '<a href="/portal/browse/portal/' + type + '/objects/' + id + '">More</a>' +  
            '</div></div>';

        google.maps.event.addListener(marker, 'click', function() {
            if (infowindow)
                infowindow.close()
             
            infowindow = new google.maps.InfoWindow({content: contentString});
            infowindow.open(map, marker);
          });

        if (panto) 
            map.panTo(latlng);
        
        return 1;
    } else {
        return 0;
    }
}

function initializeMap() {
    // Center on center of Black Rock Forest
    var latlng = new google.maps.LatLng(41.40744, -74.01457);
    var myOptions = {
            zoom: 13,
            center: latlng,
            mapTypeId: google.maps.MapTypeId.HYBRID
            };
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
}

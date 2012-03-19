function addBlock(mapInstance) {
    var map_bounds = new google.maps.LatLngBounds();
    
    block_json = JSON.parse(jQuery('#block_json')[0].innerHTML);
    trap_sites = JSON.parse(jQuery('#trap_sites')[0].innerHTML);
    for (var i = 0; i < trap_sites.length; i++) {
        trap_info = trap_sites[i];
            m = amarker (trap_info['point'], mapInstance)
            
            m.setTitle  (trap_info['point_id'].toString());
            
            attach_marker_info (m, trap_info);
    }
    var box = block_json;
    var rect = make_grid_rectangle (bounds (block_json), mapInstance);
    map_bounds.extend(lat_lng_from_point(box[0] ));
    map_bounds.extend(lat_lng_from_point(box[1] ));
    map_bounds.extend(lat_lng_from_point(box[2] ));
    map_bounds.extend(lat_lng_from_point(box[3] ));
    
    viewer_location = user_location(mapInstance);
    
    if (viewer_location ) {
        you_are_here (viewer_location);
    }
    
    if (!map_bounds.isEmpty() ) {
        mapInstance.fitBounds(map_bounds);
    } 
}


function attach_marker_info(marker, info) {
    google.maps.event.addListener(marker, 'mouseover', function() {
        jQuery ('#point_' + info['point_id']).addClass("highlighted");
    });
  
    google.maps.event.addListener(marker, 'mouseout', function() {
        jQuery ('#point_' + info['point_id']).removeClass("highlighted");
    });
    
    jQuery ('#point_' + info['point_id']).mouseover( function () {
    
            jQuery ('#point_' + info['point_id']).addClass("highlighted");
            marker.setAnimation(google.maps.Animation.BOUNCE);
        }
    );
     jQuery ('#point_' + info['point_id']).mouseout( function () {
    
            jQuery ('#point_' + info['point_id']).removeClass("highlighted");
            marker.setAnimation(null);
        }
    );
}




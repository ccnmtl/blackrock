
function addBlock(mapInstance) {
    //var map_bounds = new google.maps.LatLngBounds();
    
    block_json = JSON.parse(jQuery('#block_json')[0].innerHTML)
    
    
    trap_sites = JSON.parse(jQuery('#trap_sites')[0].innerHTML)
    
    //alert (trap_sites);
    
    
    for (var i = 0; i < trap_sites.length; i++) {
        trap_info = trap_sites[i];
    
        //console.log (    trap_info['point']);
        //alert (JSON.stringify(trap_info))
            
            m = amarker (trap_info['point'], mapInstance)
            attach_marker_info (m, trap_info);
        
    }
    
    
    var box = block_json;
    var rect = make_grid_rectangle (bounds (block_json), mapInstance);
    
    /*
    marker = new google.maps.Marker({ 
        position: lat_lng_from_point(box[4]),
        map: mapInstance
    });
    */
    
    
    /*
    map_bounds.extend(lat_lng_from_point(box[0] ));
    map_bounds.extend(lat_lng_from_point(box[1] ));
    map_bounds.extend(lat_lng_from_point(box[2] ));
    map_bounds.extend(lat_lng_from_point(box[3] ));

    */
    
    viewer_location = user_location(mapInstance);
    
    if (viewer_location ) {
        you_are_here (viewer_location);
    }
               // http://tiur.ccnmtl.columbia.edu:54321/portal/grid_block/

    
    /*
    if (!map_bounds.isEmpty() ) {
        
        zoomChangeBoundsListener = 
            google.maps.event.addListenerOnce(mapInstance, 'bounds_changed', function(event) {
                if (this.getZoom()){
                    this.setZoom(16);
                }
        });
        
        mapInstance.fitBounds(map_bounds);
        
    } */
    
}

//closure:

function attach_marker_info(marker, info) {

    google.maps.event.addListener(marker, 'click', function() {

        str = "This point is " + info ['direction_x'] + " of center by " +  info ["distance_x"].toFixed(0) + " meters" ;
        str += "\n and "       + info ['direction_y'] + " of center by " +  info ["distance_y"].toFixed(0) + " meters." ;
        str += "\n Compass heading: " + info ['heading'].toFixed(0)  + " degrees." ;
        str += "\n Distance: " + info ['actual_distance'].toFixed(0) + " meters." ;
        alert (str);
        
  
/*    
  
    rect.setOptions ({fillOpacity : 0.3});
  
    jQuery('#bl')[0].innerHTML = trimpoint(info['box'][0]);
    jQuery('#tl')[0].innerHTML = trimpoint(info['box'][1]);
    jQuery('#tr')[0].innerHTML = trimpoint(info['box'][2]);
    jQuery('#br')[0].innerHTML = trimpoint(info['box'][3]);
    jQuery('#c') [0].innerHTML = trimpoint(info['box'][4]);
  
    jQuery('#block_info') [0].innerHTML =  'Block # ' + info['id']+ ':'
*/    
  });
  
  /*
  google.maps.event.addListener(rect, 'mouseout', function() {
    rect.setOptions ({fillOpacity : 0.1});
  });
*/
}




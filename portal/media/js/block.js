
function addBlock(mapInstance) {
    //var map_bounds = new google.maps.LatLngBounds();
    
    
    grid_json = JSON.parse(jQuery('#grid_json')[0].innerHTML)
    i = 0
    j = 0;

    var box = grid_json;
    var rect = make_grid_rectangle (bounds (box), mapInstance);
    
    var column = grid_json[i].length - j;
    /*
    marker = new google.maps.Marker({ 
        position: lat_lng_from_point(box[4]),
        map: mapInstance
    });
    */
    attach_info (rect, {
            'i':  i,
            'j':  j,
            'row':  row,
            'column':  column,
            'id' : i * grid_json.length  + column,
            'box':box
        }
    )
    
    
    map_bounds.extend(lat_lng_from_point(box[0] ));
    map_bounds.extend(lat_lng_from_point(box[1] ));
    map_bounds.extend(lat_lng_from_point(box[2] ));
    map_bounds.extend(lat_lng_from_point(box[3] ));

    
    
    viewer_location = user_location(mapInstance);
    
    if (viewer_location ) {
        you_are_here (viewer_location);
    }
    
    
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

function attach_info(rect, info) {
/*    
  google.maps.event.addListener(rect, 'mouseover', function() {
  
    rect.setOptions ({fillOpacity : 0.3});
  
    jQuery('#bl')[0].innerHTML = trimpoint(info['box'][0]);
    jQuery('#tl')[0].innerHTML = trimpoint(info['box'][1]);
    jQuery('#tr')[0].innerHTML = trimpoint(info['box'][2]);
    jQuery('#br')[0].innerHTML = trimpoint(info['box'][3]);
    jQuery('#c') [0].innerHTML = trimpoint(info['box'][4]);
  
    jQuery('#block_info') [0].innerHTML =  'Block # ' + info['id']+ ':'
    
  });
  
  google.maps.event.addListener(rect, 'mouseout', function() {
    rect.setOptions ({fillOpacity : 0.1});
  });
*/
}




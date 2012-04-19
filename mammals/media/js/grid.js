
function addGrid(mapInstance) {
    var map_bounds = new google.maps.LatLngBounds();
    grid_json = JSON.parse(jQuery('#grid_json')[0].innerHTML)
    for (var i = 0; i < grid_json.length; i++) {
        var box = grid_json[i]['corner_obj'];
        var rect = make_grid_rectangle (bounds (box), mapInstance);
        
        //result['corner_obj'] = self.corner_obj()
        //result['label']      = self.label_2
        
        //console.log (grid_json[i]);
        //console.log (box);
        
        attach_info (rect, {
                'id' :grid_json[i]['label'],
                'box':grid_json[i]['corner_obj']
            }   
        );
        map_bounds.extend(lat_lng_from_point(box[4] ));
        
    
    }
    
    
    // this works but it's really annoying.
    /*
    viewer_location = user_location(mapInstance);
    if (viewer_location ) {
        you_are_here (viewer_location);
    }
    */
    
    if (!map_bounds.isEmpty() ) {
        mapInstance.fitBounds(map_bounds);
    } 
}


//closure:
function attach_info(rect, info) {
  google.maps.event.addListener(rect, 'mouseover', function() {
  
    rect.setOptions ({fillOpacity : 0.3});
  
    jQuery('#bl')[0].innerHTML = trimpoint(info['box'][0]);
    jQuery('#tl')[0].innerHTML = trimpoint(info['box'][1]);
    jQuery('#tr')[0].innerHTML = trimpoint(info['box'][2]);
    jQuery('#br')[0].innerHTML = trimpoint(info['box'][3]);
    jQuery('#c') [0].innerHTML = trimpoint(info['box'][4]);
    
    
    jQuery('#selected_block_center_y') [0].value = info['box'][4][0];
    jQuery('#selected_block_center_x') [0].value = info['box'][4][1];
    
  
    jQuery('#block_info') [0].innerHTML =  'Square # ' + info['id']+ ':'
    
  });
  
  google.maps.event.addListener(rect, 'mouseout', function() {
    rect.setOptions ({fillOpacity : 0.1});
  });
  
  
  google.maps.event.addListener(rect, 'click', function() {
    
     jQuery('#grid_form')[0].action =   '/mammals/grid_square/';
     jQuery('#grid_form')[0].submit();
 
  });
  
  

}


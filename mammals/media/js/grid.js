var grid_json;


function addGrid(mapInstance) {
    var map_bounds = new google.maps.LatLngBounds();
    grid_json = JSON.parse(jQuery('#grid_json')[0].innerHTML)
    
    //alert (JSON.stringify(grid_json[0]));
    //return;
    
    for (var i = 0; i < grid_json.length; i++) {
        var box = grid_json[i]['corner_obj'];
        var rect = make_grid_rectangle (bounds (box), mapInstance);
        
        //result['corner_obj'] = self.corner_obj()
        //result['label']      = self.label_2
        //console.log (grid_json[i]);
        //console.log (box);
        
        attach_info (rect, {
                'box':     grid_json[i]['corner_obj'],
                'row' :    grid_json[i]['row'],
                'column' : grid_json[i]['column'],
                'label':   grid_json[i]['label'],
            }   
        );
        map_bounds.extend(lat_lng_from_point(box[4] ));
        grid_json [i]['grid_rectangle'] = rect
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


function suggest_square() {
    suggested_square = grid_json[Math.floor(Math.random()*grid_json.length)].grid_rectangle;
    decorate_suggested_square (suggested_square);
}

function unsuggest_square() {
    if (typeof(undecorate_suggested_square) == "function") {
        undecorate_suggested_square();
    }
}

function decorate_suggested_square (suggested_square) {
    var selected_style = {fillOpacity : 0.6, 
        fillColor       : 'red',}
    var unselected_style = {fillOpacity : 0.1,
        fillColor       : 'blue',}
    unsuggest_square();
    suggested_square.setOptions (selected_style);
    undecorate_suggested_square = function () {
        suggested_square.setOptions (unselected_style);
    }
}




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
    
  
    jQuery('#block_info') [0].innerHTML =  'Square # ' + info['label']+ ':'
    
    jQuery('.grid_border_coords_table').show();
    
    //jQuery('#block_info') [0].innerHTML =  'Row : ' + info['row']+ ' and column ' +  info['column'] + " and label" +  info['label'] + " and label_2 " +  info['label_2']
    
    
  });
  
  google.maps.event.addListener(rect, 'mouseout', function() {
    rect.setOptions ({fillOpacity : 0.1});
  });
  
  
  google.maps.event.addListener(rect, 'click', function() {
     the_form = jQuery('#grid_form')[0]
     if (is_sandbox()) {
         the_form.action =   '/mammals/sandbox/grid_square/';
    } else {
        the_form.action =   '/mammals/grid_square/';
    }
     the_form.submit();
 
  });

}




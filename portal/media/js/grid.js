
function addGrid(mapInstance) {
    // AT LATITUDE 40 DEGREES (NORTH OR SOUTH)
    // http://www.zodiacal.com/tools/lat_table.php
    // One degree of latitude =  111.03 km or  68.99 mi
    // One degree of longitude =  85.39 km or  53.06 mi
    /*
    one_lat_degree  = 111.03; // km
    one_long_degree = 85.39;  // km
    radius_km = 1.0;
    number_of_markers = 25;
    var brf_x  =    41.397459;
    var brf_y  =   -74.021848;
    radius_x =  radius_km / one_lat_degree  ;
    radius_y =  radius_km / one_long_degree ;
    for (var i = 0; i < number_of_markers  ; i++) {
        theta =  i * Math.PI / number_of_markers * 2;
        var x = brf_x  + Math.sin(theta) * radius_x;
        var y = brf_y  + Math.cos(theta) * radius_y ;
        var location = new google.maps.LatLng(x,y);
        //console.log(location);
        marker = new google.maps.Marker({
            position: location,
            map: mapInstance
        });
   }
   */
   /*
    circle_points = JSON.parse(jQuery('#circle')[0].innerHTML)
    for (var i = 0; i < circle_points.length  ; i++) {
        var location = new google.maps.LatLng(circle_points[i].x ,circle_points[i].y);
        marker = new google.maps.Marker({
            position: location,
            map: mapInstance
        });
    }
    */
    grid_json = JSON.parse(jQuery('#grid_json')[0].innerHTML)
    
    
    for (var i = 0; i < grid_json.length; i++) {
        //console.log (grid_json[i]);
        for (var j = 0; j < grid_json[i].length; j++) {
            
            //console.log (grid_json[i][j][0]);
            //console.log (grid_json[i][j][1]);
            var location_1 = new google.maps.LatLng(grid_json[i][j][0][0] , grid_json[i][j][0][1]);
            var location_2 = new google.maps.LatLng(grid_json[i][j][1][0] , grid_json[i][j][1][1]);
            var location_3 = new google.maps.LatLng(grid_json[i][j][2][0] , grid_json[i][j][2][1]);
            var location_4 = new google.maps.LatLng(grid_json[i][j][3][0] , grid_json[i][j][3][1]);
            var location_5 = new google.maps.LatLng(grid_json[i][j][4][0] , grid_json[i][j][4][1]);
            
            /*
            marker = new google.maps.Marker({ position: location_1, map: mapInstance });
            marker = new google.maps.Marker({ position: location_2, map: mapInstance });
            marker = new google.maps.Marker({ position: location_3, map: mapInstance });
            marker = new google.maps.Marker({ position: location_4, map: mapInstance });
            */
            
            //marker = new google.maps.Marker({ position: location_1, map: mapInstance });
            
            // commenting out during grid refactor
            // make_grid_rectangle ([ location_1, location_2, location_3, location_4], mapInstance);
            
            /*
            rect = new google.maps.Rectangle ()
            rect.setBounds (new google.maps.LatLngBounds( location_1, location_3 ));
            */
            
            marker = new google.maps.Marker({ position: location_5, map: mapInstance });
        
        }
    }
    
    //center = JSON.parse(jQuery('#center')[0].innerHTML)
    //before = JSON.parse(jQuery('#before')[0].innerHTML)
    //after  = JSON.parse(jQuery('#after' )[0].innerHTML)
    
    //center_location = new google.maps.LatLng(center[0], center[1]);
    //before_location = new google.maps.LatLng(before[0], before[1]);
    //after_location  = new google.maps.LatLng(after [0], after [1]);
   

    //marker = new google.maps.Marker({ position: before_location, map: mapInstance });
    //marker = new google.maps.Marker({ position: center_location, map: mapInstance });
    //marker = new google.maps.Marker({ position: after_location, map: mapInstance });
    
}

function make_grid_rectangle (paths, mapInstance) {
    rect = new google.maps.Polygon ({
        paths : [ location_1, location_2, location_3, location_4],
        fillOpacity : 0.1,
        fillColor : 'blue',
        strokeOpacity : 0.3,
        strokeColor : 'green',
        strokeWeight : 1
    });
    rect.setMap    (mapInstance);     
}

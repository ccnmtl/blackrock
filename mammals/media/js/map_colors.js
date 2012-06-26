
square_styles = {
    'regular': {
        'selected' : { // mouseover
            fillOpacity     : 0.3
            ,fillColor      : 'blue'
            ,strokeOpacity   : 0.3
            ,strokeColor     : 'green'
            ,strokeWeight    : 1
        }
        
        // note square_styles.regular.unselected is also used
        // for the one-square view on the square page.
        ,'unselected' : { //not mouseover
            fillOpacity     : 0.1
            ,fillColor      : 'blue'
            ,strokeOpacity   : 0.3
            ,strokeColor     : 'green'
            ,strokeWeight    : 1
        }
    }

    ,'hidden' : { // cause they don't meet the conditions of the filter
        'selected' : {
            fillOpacity     : 0.0
            ,strokeOpacity     : 0.0
        }
        ,'unselected' : {
            fillOpacity     : 0.0
            ,strokeOpacity     : 0.0
        }
    }
    ,'suggested_square' : { // suggested by the randomize button
        'selected' : { // mouseover
            fillOpacity     : 1.0
            ,fillColor      : 'red'
            ,strokeOpacity   : 0.3
            ,strokeColor     : 'green'
        }
        ,'unselected' : { //not mouseover
            fillOpacity     : 0.6
            ,fillColor      : 'red'
            ,strokeOpacity   : 0.3
            ,strokeColor     : 'green'
        }
    }
    
    
    ,'just_visited': {
        'selected' : { // mouseover
            fillOpacity     : 0.8
            ,fillColor      : 'purple'
            ,strokeOpacity   : 0.3
            ,strokeColor     : 'green'
        }
        ,'unselected' : { //not mouseover
            fillOpacity     : 0.6
            ,fillColor      : 'purple'
            ,strokeOpacity   : 0.3
            ,strokeColor     : 'green'
        }
    }
    
}


initial_circle_style = {
      radius: 2, // this is the radius in meters on the surface of the planet.
      fillColor: 'lightgreen',
      fillOpacity : 1,
      strokeWeight : 1,
      strokeColor : 'lightgreen',
      strokeOpacity : 1,
      zIndex: 1
}

circle_on_style = {
    fillColor : "blue",
    radius: 5,
    zIndex: 1
}

circle_off_style = {
    fillColor : "lightgreen",
    radius: 2,
    zIndex: 2
}


// These 3 styles are used in the minimaps in the team form page.
mini_map_center_style = {
      radius: 2, // this is the radius in meters on the surface of the planet.
      fillColor: 'lightgreen',
      fillOpacity : 1,
      strokeWeight : 1,
      strokeColor : 'lightgreen',
      strokeOpacity : 1,
      zIndex: 1
}

mini_map_suggested_point_style = {
      radius: 2, // this is the radius in meters on the surface of the planet.
      fillColor: 'yellow',
      fillOpacity : 0.5,
      strokeWeight : 1,
      strokeColor : 'yellow',
      strokeOpacity : 0.5,
      zIndex: 1
}

mini_map_actual_point_style = {
      radius: 2, // this is the radius in meters on the surface of the planet.
      fillColor: 'red',
      fillOpacity : 1,
      strokeWeight : 1,
      strokeColor : 'red',
      strokeOpacity : 1,
      zIndex: 1
}


mini_map_actual_point_style = {
      radius: 2, // this is the radius in meters on the surface of the planet.
      fillColor: 'red',
      fillOpacity : 1,
      strokeWeight : 1,
      strokeColor : 'red',
      strokeOpacity : 1,
      zIndex: 1
}







initial_transect_style = {
    strokeColor : 'yellow',
    strokeOpacity : 0.5, 
    zIndex: -3
}

transect_off_style =  {
    strokeOpacity : 0.3
}

transect_on_style = {
    strokeOpacity : 1
}




mini_map_transect_1_style = {
    strokeColor : 'yellow',
    strokeOpacity : 0.8,
    zIndex: -3
}


mini_map_transect_2_style = {
    strokeColor : 'yellow',
    strokeOpacity : 0.3,
    zIndex: -3
}

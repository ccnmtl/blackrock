// These 3 styles are used in the minimaps in the team form page.
habitat_disk_style = {
      radius: 20, // this is the radius in meters on the surface of the planet.
      //fillColor: 'lightgreen',
      fillOpacity : 0.6,
      strokeWeight : 1,
      strokeColor : 'black',
      strokeOpacity : 0.6,
      zIndex: 1
}

square_styles = {
    'regular': {
        'selected' : { // mouseover
            fillOpacity     : 0.3
            ,fillColor      : '#f1ab00'
            ,strokeOpacity   : 1
            ,strokeColor     : '#985122'
            ,strokeWeight    : 1
        }
        
        // note square_styles.regular.unselected is also used
        // for the one-square view on the square page.
        ,'unselected' : { //not mouseover
            fillOpacity     : 0.0
            //,fillColor      : '#f1ab00'
            ,strokeOpacity   : 0.3
            ,strokeColor     : '#d38c0c'
            ,strokeWeight    : 1
        }
    }
}




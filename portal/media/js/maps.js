if (typeof Portal == 'undefined') {
    Portal = {};
}

if (!Portal.Base) { 
    Portal.Base = {
        'Observer' : function() {
            // the real work is done by connect/signal stuff below
            // this just keeps track of the stuff that needs to be destroyed
            var _listeners = {};
            var _named_listeners = {};
            var _nextListener = 0;
            this.addListener = function(obj, slot) {
                if (slot && _named_listeners[slot]) {
                    this.removeListener(slot);
                    _named_listeners[slot] = obj;
                    return slot;
                } else {
                    _listeners[++_nextListener] = obj;
                    return _nextListener;
                }
            };
            this.removeListener = function(slot_or_pos) {
                var stor = (_named_listeners[slot_or_pos]) ? _named_listeners
                        : _listeners;
                if (stor[slot_or_pos]) {
                    stor[slot_or_pos].disconnect();
                    delete stor[slot_or_pos];
                }
            };
            this.clearListeners = function() {
                for (a in _named_listeners) {
                    this.removeListener(a);
                }
                for (a in _listeners) {
                    this.removeListener(a);
                }
            };
            this.events = {
                signal : Portal.Base.Events.signal,
                connect : Portal.Base.Events.connect
            };
        }// Observer
    };
}

if (!Portal.Base.Events) {    
    if (typeof MochiKit != 'undefined') {
        Portal.Base.Events = {
            'connect' : function(subject, event, self, func) {
                if (typeof subject.nodeType != 'undefined' || subject == window
                        || subject == document) {
                    event = 'on' + event;
                }
                var disc = MochiKit.Signal.connect(subject, event, self, func);
                return {
                    disconnect : function() {
                        MochiKit.Signal.disconnect(disc);
                    }
                }
            },
            'signal' : function(subject, event, param) {
                MochiKit.Signal.signal(subject, event, param);
            }
        }
    } //mochikit
    else if (typeof jQuery != 'undefined') {
        Portal.Base.Events = {
            'connect' : function(subject, event, self, func) {
                var disc = jQuery(subject).bind(event, function() {
                    func.call(self, event, this);
                });
                return {
                    disconnect : function() {
                        disc.unbind(event);
                    }
                }
            },
            'signal' : function(subject, event) {
                jQuery(subject).trigger(event);
            }
        }
    } //jquery
    else if (typeof YUI != 'undefined') {

    }//YUI
    else {
        throw Error("Use a framework, Dude! MochiKit, jQuery, YUI, whatever!");
    }    
}

if (!Portal.Layer) {
    Portal.Layer = function(identifier, fileName, clickable) {
        var self = this;
        Portal.Base.Observer.apply(this,arguments); //inherit events
    
        self.identifier = identifier;
        
        var myOptions = { preserveViewport: "true", suppressInfoWindows: true, clickable: clickable };
        self.instance = new google.maps.KmlLayer(fileName, myOptions);
        
        google.maps.event.addListener(self.instance, 'click', function (kmlEvent) {
            self.events.signal(Portal, 'kmlClicked', kmlEvent);
        });
        
        this.isVisible = function() {
            return self.instance.map != null;
        }
        
        this.shouldBeVisible = function() {
            var element = document.getElementById(self.identifier);
            return element.checked;
        }
    }
}

if (!Portal.MapMarker) {    
    Portal.MapMarker = function() {
        var self = this;
        
        Portal.Base.Observer.apply(this,arguments); //inherit events
        self.assetIdentifier = null;
        self.description = null; 
        self.featured = [];
        self.infrastructure = [];
        self.marker = null;
        self.latlng = null;
        
        this.create = function(mapInstance, assetIdentifier, name, description, lat, lng, featured, infrastructure, iconName, zIndex) {
            self.assetIdentifier = assetIdentifier;;
            self.description = description; 
            self.featured = featured;
            self.infrastructure = infrastructure;
            
            if (!lat || !lng)
                return null;
            
            var iconUrl = '';
            if (infrastructure && infrastructure.length) {
                var iconName = infrastructure[0];
                iconName = iconName.replace(/ /g, "");
                iconName = iconName.replace("-", "");
                iconUrl = 'http://' + location.hostname + ':' + location.port + "/portal/media/images/mapicon_" + iconName.toLowerCase() + '.png';
            } else if (featured && featured.length) {
                var iconName = featured[0];
                iconName = iconName.replace("Featured ", "");
                iconUrl = 'http://' + location.hostname + ':' + location.port + "/portal/media/images/mapicon_" + iconName.toLowerCase() + '.png';
            } else if (iconName) {
                if (iconName.indexOf("http:") === 0)
                    iconUrl = iconName;
                else
                    iconUrl = 'http://' + location.hostname + ':' + location.port + "/portal/media/images/" + iconName;
            } else {
                iconUrl = 'http://' + location.hostname + ':' + location.port + "/portal/media/images/mapicon_main.png";
            }

            self.latlng = new google.maps.LatLng(lat, lng);
            var shouldBeVisible = self.shouldBeVisible();
            self.marker = new google.maps.Marker({
                position: self.latlng, 
                title: name,
                icon: iconUrl,
                map: shouldBeVisible ? mapInstance : null,
                zIndex: zIndex
             });
            
            google.maps.event.addListener(self.marker, 'click', function() {
               self.events.signal(Portal, 'markerClicked', self.assetIdentifier);
            });
            
            return self.latlng;
        }
        
        this.isVisible = function() {
            return self.marker.map != null;
        }
        
        this.shouldBeVisible = function() {
            var visible = false;
            var options = null;
            var values = null;
            
            if (self.infrastructure && self.infrastructure.length ) {
                options = getElementsByTagAndClassName("input", "infrastructure_option");
                values = self.infrastructure;
            } else if (self.featured && self.featured.length) {
                options = getElementsByTagAndClassName("input", "featured_option");
                values = self.featured;
            } else {
                visible = true;
            }

            if (options) {
                forEach(options,
                        function(option) {
                            if (option.checked) {
                                for (var i=0; i < values.length; i++) {
                                    if (option.value == values[i]) {
                                        visible = true;
                                    }
                                }
                            }
                        });
            }
                
            return visible;
        }
    }
}

if (!Portal.Map) {
    Portal.Map = function() {
        var self = this;
        
        Portal.Base.Observer.apply(this,arguments); //inherit events
        
        self.mapInstance = null;
        self.locations = {};
        self.search_results = {};
        self.infoWindow = null;
        self.layers = {}
        
        this.hideInfoWindow = function() {
            if (self.infowindow)
                self.infowindow.close()
        }

        this.showLayerInfoWindow = function(kmlEvent) {
            if (self.infowindow)
                self.infowindow.close()
            
            var description;

            // @todo -- client-side templates?
            if (kmlEvent.featureData.name) {
                description =  '<div class="callout"><span class="callout-display-name">' + kmlEvent.featureData.name + '</span>';
                if (kmlEvent.featureData.description)
                    description += '<div class="callout-asset-types">' + kmlEvent.featureData.description + '</div>';
                description += '<a class="callout-summary-link" onclick="portalMapInstance.search(' + 
                               kmlEvent.latLng.lat() + ', ' + kmlEvent.latLng.lng() + ', \'' + escape(kmlEvent.featureData.name) + '\')">Search nearby</a></div>';
            } else if (kmlEvent.featureData.description) {
                var title = kmlEvent.featureData.description.replace("_blank", "_self");
                description =  '<div class="callout"><div>' + title + '</div><br />';
                title = title.replace(/(<([^>]+)>)/ig,"");
                description += '<a class="callout-summary-link" onclick="portalMapInstance.search(' + 
                               kmlEvent.latLng.lat() + ', ' + kmlEvent.latLng.lng() + ', \'' + escape(title) + '\')">Search nearby</a></div>';                
            } else {
                description = kmlEvent.latLng.lat() + ', ' + kmlEvent.latLng.lng();
            }
            
            var params = {content: description, position: kmlEvent.latLng, maxWidth: 400 }
            if (kmlEvent.pixelOffset.height < 0)
                params['pixelOffset'] = new google.maps.Size(-5, -20);
            self.infowindow = new google.maps.InfoWindow(params);
            self.infowindow.open(self.mapInstance);
        }
        
        this.showMarkerInfoWindow = function(asset_identifier) {
            var location = self.locations[asset_identifier];
            if (!location)
                location = self.search_results[asset_identifier]
            if (!location && self.selected)
                location = self.selected[asset_identifier];
            
            if (location) {

                if (self.infowindow)
                    self.infowindow.close()
                
                var offset = new google.maps.Size(-5, 15);
    
                self.infowindow = new google.maps.InfoWindow({content: location.description, maxWidth: 400, pixelOffset: offset });
                self.infowindow.open(self.mapInstance, location.marker);
            }
        }
        
        this.toggleFacet = function() {
            for (var assetIdentifier in self.locations) {
                var location = self.locations[assetIdentifier];
                var visible = location.isVisible();
                var shouldBeVisible = location.shouldBeVisible();
                
                if (shouldBeVisible && !visible) {
                    location.marker.setMap(self.mapInstance);
                } else if (!shouldBeVisible && visible) {
                    location.marker.setMap(null);
                }
            }
        }
        
        this.toggleLayer = function() {
            for (var identifier in self.layers) {
                var layer = self.layers[identifier];
                var visible = layer.isVisible();
                var shouldBeVisible = layer.shouldBeVisible();
                
                if (shouldBeVisible && !visible) {
                    layer.instance.setMap(self.mapInstance);
                } else if (!shouldBeVisible && visible) {
                    layer.instance.setMap(null);
                }
            }
        }
        
        this.initMarkers = function(className, zIndexBoost, fitBounds) {
            // iterate over locations within the page, and add the requested markers
            var bounds = new google.maps.LatLngBounds();
            var a = {};
            var elements = getElementsByTagAndClassName("div", className);
            var zIndex = 100 + zIndexBoost;
            forEach(elements,
                    function(elem) {
                        var assetIdentifier = getFirstElementByTagAndClassName(null, "asset_identifier", elem).value;
                        var name = document.getElementById(assetIdentifier + "-name").value;
                        var description = document.getElementById(assetIdentifier + "-description").innerHTML;
                        var latitude = document.getElementById(assetIdentifier + "-latitude").value;
                        var longitude = document.getElementById(assetIdentifier + "-longitude").value;
                        
                        var iconname = null;
                        var property = document.getElementById(assetIdentifier + "-iconname");
                        if (property && property.value.length > 0)
                            iconname = property.value;
                        
                        var featured = null;
                        var infrastructure = null;
                        
                        property = document.getElementById(assetIdentifier + "-infrastructure");
                        if (property && property.value.length > 0)
                            infrastructure = property.value.split(",")
                            
                        property = document.getElementById(assetIdentifier + "-featured");
                        if (property && property.value.length > 0)
                            featured = property.value.split(",")
                        
                        var marker = new Portal.MapMarker();
                        var latlng = marker.create(self.mapInstance, assetIdentifier, name, description, latitude, longitude, featured, infrastructure, iconname, zIndex);
                        
                        a[assetIdentifier] = marker;
                        bounds.extend(latlng);
                        zIndex--;
                    });      
            
            if (!bounds.isEmpty() && fitBounds)
                self.mapInstance.fitBounds(bounds);
            
            return a;
        }
        
        this.search = function(lat, long, title) {
            for (var result in self.search_results) {
                var location = self.search_results[result];
                location.marker.setMap(null);
            }
            self.search_results = {};
            
            document.getElementById("map_filters").style.display = "none";
            
            var nearby_results = document.getElementById("nearby_results");
            
            jQuery(nearby_results).show('fast', function() {
                var url = '/portal/nearby/' + lat + '/' + long + '/';
                var request = doXHR(url);
                request.addCallback(function(response) {
                    nearby_results.innerHTML = response.responseText;
                    document.getElementById("nearby_asset").innerHTML = unescape(title);
                    self.search_results = self.initMarkers("nearby", 0, true);
                    
                    var listener = google.maps.event.addListenerOnce(self.mapInstance, "idle", function() { 
                        var center = new google.maps.LatLng(lat, long);
                        self.mapInstance.setCenter(center);
                    });
                    
                });
            });
        }
        
        this.closeSearch = function() {
            document.getElementById("map_filters").style.display = "block";
            var nearby_results = document.getElementById("nearby_results");
            nearby_results.innerHTML = "";
            nearby_results.style.display = "none";
            
            for (var result in self.search_results) {
                var location = self.search_results[result];
                location.marker.setMap(null);
            }
            self.search_results = {};
            self.center();
        }
        
        this.center = function() {
            var latlng = new google.maps.LatLng(41.397459,-74.021848);
            self.mapInstance.setCenter(latlng);
            self.mapInstance.setZoom(13);
        }
        
        this.markerCount = function(myobj) {
            var count = 0;
            for (k in myobj) if (myobj.hasOwnProperty(k)) count++;
            return count;
        }
        
        this.init = function() {
            if (!document.getElementById("map_canvas"))
                return;

            // Center on center of Black Rock Forest
            var latlng = new google.maps.LatLng(41.397459,-74.021848);
            var myOptions = {
                zoom: 13,
                center: latlng,
                mapTypeId: google.maps.MapTypeId.TERRAIN
            };
            
            self.mapInstance = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
            
            self.events.connect(Portal, 'markerClicked', self, 'showMarkerInfoWindow');
            self.events.connect(Portal, 'kmlClicked', self, 'showLayerInfoWindow');
            self.events.connect(Portal, 'toggleFacet', self, 'toggleFacet');
            self.events.connect(Portal, 'toggleLayer', self, 'toggleLayer');
            
            var randomnumber=Math.floor(Math.random()*100000);
            var options = getElementsByTagAndClassName("input", "layer");
            forEach(options,
                    function(option) {
                        var kmllayer = new Portal.Layer(option.id, "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/" + option.id + ".kml?grrrr=" + randomnumber, true);
                        self.layers[option.id] = kmllayer;
                        
                        connect(option, 'onclick', function(evt) {
                            self.events.signal(Portal, 'toggleLayer');
                         });
                    });
            
            options = getElementsByTagAndClassName("input", "facet");
            forEach(options,
                    function(option) {
                        connect(option, 'onclick', function(evt) {
                            self.events.signal(Portal, 'toggleFacet');
                         });
                    });
                
            self.locations = self.initMarkers("geocode", 0, false);
            var detail_locations = self.initMarkers("geocode_detail", 0, true);
            for (var key in detail_locations)
                self.locations[key] = detail_locations[key];
            
            self.selected = self.initMarkers("geoselected", 0, true);
            if (self.markerCount(self.selected)) {
                var listener = google.maps.event.addListenerOnce(self.mapInstance, "idle", function() { 
                    self.mapInstance.setZoom(14);
                    
                    for (var s in self.selected) {
                        self.showMarkerInfoWindow(s);
                    }
                });
            }
            
            var boundary = new Portal.Layer("brfboundary", "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/brfboundary.kml?newcachebuster=" + randomnumber, false);
            boundary.instance.setMap(self.mapInstance);

            self.toggleLayer();
            addGrid(self.mapInstance);
            
            
        }
    }
}

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
            
            
            rect = new google.maps.Polygon ({
                paths : [ location_1, location_2, location_3, location_4],
                fillOpacity : 0.1,
                fillColor : 'blue',
                strokeOpacity : 0.3,
                strokeColor : 'green',
                strokeWeight : 1
            });
            
            rect.setMap    (mapInstance);
            
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



var portalMapInstance = null;
addLoadEvent(function() {
    portalMapInstance = new Portal.Map();
    portalMapInstance.init();
    
    
    var latlng = new google.maps.LatLng(41.397459,-74.021848);
});




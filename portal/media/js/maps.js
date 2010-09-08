/*

var map = null;
var infowindow = null;
var asset2Detail = {};

function toggleInfrastructureMarkers() {
    log('toggleInfrastructureMarkers');
    var options = getElementsByTagAndClassName("input", "infrastructure_option");
    forEach(options,
            function(option) {
                log("Option: " + option.value);
            }
            );
    
    log(options);
    for (var k = 0; k < options.length; k++)
        log("Option Value: " + options[k].value);
    
    for (var key in asset2Detail) {
        detail = asset2Detail[key];
        if (detail.infrastructure) {
            
            var show = false;
            for (var i=0; i < detail.infrastructure.length; i++) {
                for (var j=0; j < options.length; j++) {
                    if (!show && options[j].checked) 
                        show = true;
                }
            }
            
            if (show) {
                detail['marker'].map = map;
            } else {
                detail['marker'].map = null;
            }
        }
    }
}

function showInfoWindow(asset_id) {
    var callout = asset2Detail[asset_id];
    var latlng = new google.maps.LatLng(callout['latitude'], callout['longitude']);
    
    if (infowindow)
        infowindow.close()
    
    var offset = new google.maps.Size(0,-30);

    infowindow = new google.maps.InfoWindow({content: callout['content'], position: latlng, pixelOffset: offset});
    infowindow.open(map);
}

function addMarker(asset_identifier, description, lat, lng, audiences, infrastructure) {
    var marker = null;
    if (lat && lng) {
        var latlng = new google.maps.LatLng(lat, lng);
        
        var iconUrl = '';
        if (infrastructure && infrastructure.length) {
            var iconName = infrastructure[0];
            iconName = iconName.replace(" ", "");
            iconName = iconName.replace("-", "");
            iconUrl = 'http://' + location.hostname + ':' + location.port + "/portal/media/images/mapicon_" + iconName.toLowerCase() + '.png';
        } else if (audiences && audiences.length) {
            
        }
        
        var marker = new google.maps.Marker({
            position: latlng, 
            map: map, 
            title: name,
            icon: iconUrl
        }); 
        
        asset2Detail[asset_identifier] = { 
                "content": description, 
                "latitude": lat, 
                "longitude": lng, 
                "marker": marker,
                "audiences": audiences,
                "infrastructure": infrastructure };
        
        google.maps.event.addListener(marker, 'click', function() {
            showInfoWindow(asset_identifier);
          });
        
        return 1;
    } else {
        return 0;
    }
}

function initializeMap() {
    
    if (!document.getElementById("map_canvas")) {
        return;
    }
   
    // Center on center of Black Rock Forest
    var latlng = new google.maps.LatLng(41.40744, -74.01457);
    var myOptions = {
        zoom: 13,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.HYBRID
        };
    
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
    
    // iterate over locations within the page, and add the requested markers
    // locations are identified as <div class="geocode"
    elements = getElementsByTagAndClassName(null, "geocode");
    forEach(elements,
            function(elem)
            {
                var asset_identifier = getFirstElementByTagAndClassName(null, "asset_identifier", elem).value;
                var description = document.getElementById(asset_identifier + "-description").innerHTML;
                var latitude = document.getElementById(asset_identifier + "-latitude").value;
                var longitude = document.getElementById(asset_identifier + "-longitude").value;
                
                var audiences = null;
                var infrastructure = null;
                
                var property = document.getElementById(asset_identifier + "-audience").value;
                if (property && property.length > 0)
                    audiences = property.split(",")
                
                property = document.getElementById(asset_identifier + "-infrastructure").value;
                if (property && property.length > 0)
                    infrastructure = property.split(",")
                
                addMarker(asset_identifier, description, latitude, longitude, audiences, infrastructure);
            });
}


**/

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

if (!Portal.MapMarker) {
    
    Portal.MapMarker = function() {
        var self = this;
        
        Portal.Base.Observer.apply(this,arguments); //inherit events
        
        self.assetIdentifier = null;
        self.description = null; 
        self.audiences = [];
        self.infrastructure = [];
        self.marker = null;
        
        this.create = function(mapInstance, assetIdentifier, name, description, lat, lng, audiences, infrastructure) {
            self.assetIdentifier = assetIdentifier;;
            self.description = description; 
            self.audiences = audiences;
            self.infrastructure = infrastructure;
            
            if (!lat || !lng)
                return false;
            
            var iconUrl = '';
            if (infrastructure && infrastructure.length) {
                var iconName = infrastructure[0];
                iconName = iconName.replace(" ", "");
                iconName = iconName.replace("-", "");
                iconUrl = 'http://' + location.hostname + ':' + location.port + "/portal/media/images/mapicon_" + iconName.toLowerCase() + '.png';
            } else if (audiences && audiences.length) {
                
            }

            var shouldBeVisible = self.shouldBeVisible();
            self.marker = new google.maps.Marker({
                position: new google.maps.LatLng(lat, lng), 
                title: name,
                icon: iconUrl,
                map: shouldBeVisible ? mapInstance : null,
             });
            
            log("Marker: " + name + " " + shouldBeVisible);
            
            google.maps.event.addListener(self.marker, 'click', function() {
               self.events.signal(Portal, 'markerClicked', self.assetIdentifier);
            });
            
            return true;
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
            } else if (self.audiences && self.audiences.length) {
                visible = true; // not yet implemented
                //options = getElementsByTagAndClassName("input", "audience_option");
                //values = self.audiences;
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
        self.infoWindow = null;
        
        this.showInfoWindow = function(asset_identifier) {
            var location = self.locations[asset_identifier];
            
            if (self.infowindow)
                self.infowindow.close()
            
            var offset = new google.maps.Size(0,-30);

            self.infowindow = new google.maps.InfoWindow({content: location.description, position: location.marker.position, pixelOffset: offset});
            self.infowindow.open(self.mapInstance);
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
        
        addLoadEvent(function() {
            log("Portal.Map.onLoad");
            if (!document.getElementById("map_canvas"))
                return;
           
            // Center on center of Black Rock Forest
            var latlng = new google.maps.LatLng(41.40744, -74.01457);
            var myOptions = {
                zoom: 13,
                center: latlng,
                mapTypeId: google.maps.MapTypeId.HYBRID
            };
            
            self.mapInstance = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
            
            self.events.connect(Portal, 'markerClicked', self, 'showInfoWindow');
            self.events.connect(Portal, 'toggleFacet', self, 'toggleFacet');
            
            var options = getElementsByTagAndClassName("input", "infrastructure_option");
            forEach(options,
                    function(option) {
                        connect(option, 'onclick', function(evt) {
                            self.events.signal(Portal, 'toggleFacet');
                         });
                    });
            
            // iterate over locations within the page, and add the requested markers
            // locations are identified as <div class="geocode"
            elements = getElementsByTagAndClassName(null, "geocode");
            forEach(elements,
                    function(elem)
                    {
                        var assetIdentifier = getFirstElementByTagAndClassName(null, "asset_identifier", elem).value;
                        var name = document.getElementById(assetIdentifier + "-name").value;
                        var description = document.getElementById(assetIdentifier + "-description").innerHTML;
                        var latitude = document.getElementById(assetIdentifier + "-latitude").value;
                        var longitude = document.getElementById(assetIdentifier + "-longitude").value;
                        
                        var audiences = null;
                        var infrastructure = null;
                        
                        var property = document.getElementById(assetIdentifier + "-audience");
                        if (property && property.value.length > 0)
                            audiences = property.value.split(",")
                        
                        property = document.getElementById(assetIdentifier + "-infrastructure");
                        if (property && property.value.length > 0)
                            infrastructure = property.value.split(",")
                        
                        var marker = new Portal.MapMarker();
                        marker.create(self.mapInstance, assetIdentifier, name, description, latitude, longitude, audiences, infrastructure);
                        self.locations[assetIdentifier] = marker;
                    });
         });
    }
}

var portalMapInstance = new Portal.Map();

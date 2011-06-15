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
                iconName = iconName.replace(" ", "");
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

            var latlng = new google.maps.LatLng(lat, lng);
            var shouldBeVisible = self.shouldBeVisible();
            self.marker = new google.maps.Marker({
                position: latlng, 
                title: name,
                icon: iconUrl,
                map: shouldBeVisible ? mapInstance : null,
                zIndex: zIndex
             });
            
            google.maps.event.addListener(self.marker, 'click', function() {
               self.events.signal(Portal, 'markerClicked', self.assetIdentifier);
            });
            
            return latlng;
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
                
            if (kmlEvent.featureData.name) {
                var description = '<div class="callout"><span class="callout-display-name">' + kmlEvent.featureData.name + '</span>';
                if (kmlEvent.featureData.description)
                    description += '<div class="callout-asset-types">' + kmlEvent.featureData.description + '</div>';
                description += '<a class="callout-summary-link" onclick="portalMapInstance.search(' + 
                               kmlEvent.latLng.lat() + ', ' + kmlEvent.latLng.lng() + ', \'' + escape(kmlEvent.featureData.name) + '\')">Search nearby</a></div>';
                
                self.infowindow = new google.maps.InfoWindow({content: description, position: kmlEvent.latLng, maxWidth: 400 });
                self.infowindow.open(self.mapInstance);
            }
        }
        
        this.showMarkerInfoWindow = function(asset_identifier) {
            var location = self.locations[asset_identifier];
            if (!location)
                location = self.search_results[asset_identifier]
            
            if (location) {

                if (self.infowindow)
                    self.infowindow.close()
                
                var offset = new google.maps.Size(0,-20);
    
                self.infowindow = new google.maps.InfoWindow({content: location.description, maxWidth: 400 });
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
        
        this.initMarkers = function(className, zIndexBoost) {
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
            
            if (!bounds.isEmpty())
                self.mapInstance.fitBounds(bounds);
            
            return a;
        }
        
        this.search = function(lat, long, title) {
            self.hideInfoWindow();
            
            for (var result in self.search_results) {
                var location = self.search_results[result];
                location.marker.setMap(null);
            }
            self.search_results = {};
            
            var nearby_results = document.getElementById("nearby_results");
            var center = new google.maps.LatLng(lat, long);
            
            jQuery(nearby_results).show('fast', function() {
                var url = '/portal/nearby/' + lat + '/' + long + '/';
                var request = doXHR(url);
                request.addCallback(function(response) {
                    nearby_results.innerHTML = response.responseText;
                    document.getElementById("nearby_asset").innerHTML = unescape(title);
                    self.search_results = self.initMarkers("nearby", 1000);
                    self.mapInstance.setCenter(center);
                });
            });
        }
        
        this.closeSearch = function() {
            var nearby_results = document.getElementById("nearby_results");
            nearby_results.innerHTML = "";
            nearby_results.style.display = "none";
            
            for (var result in self.search_results) {
                var location = self.search_results[result];
                location.marker.setMap(null);
            }
            self.search_results = {};
            
            var latlng = new google.maps.LatLng(41.40744, -74.01457);
            self.mapInstance.setCenter(latlng);
            self.mapInstance.setZoom(13);
        }
        
        addLoadEvent(function() {
            if (!document.getElementById("map_canvas"))
                return;

            // Center on center of Black Rock Forest
            var latlng = new google.maps.LatLng(41.40744, -74.01457);
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
            
            var randomnumber=Math.floor(Math.random()*11)
            
            // add default layers
            var kmlLayer = new Portal.Layer("boundary", "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/brfboundary.kml", false /* clickable */);
            self.layers.boundary = kmlLayer;
            
            var kmlLayer = new Portal.Layer("peaks", "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/peaks.kml?foo=" + randomnumber, true);
            self.layers.peaks = kmlLayer;
            
            kmlLayer = new Portal.Layer("ponds", "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/ponds.kml?foo=" + randomnumber, true);
            self.layers.ponds = kmlLayer;
            
            kmlLayer = new Portal.Layer("roads", "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/roads.kml?foo=" + randomnumber, true);
            self.layers.roads = kmlLayer;
            
            kmlLayer = new Portal.Layer("streams", "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/streams.kml?foo=" + randomnumber, true);
            self.layers.streams = kmlLayer;
            
            kmlLayer = new Portal.Layer("trails", "http://blackrock.ccnmtl.columbia.edu/portal/media/kml/trails.kml?foo=" + randomnumber, true);
            self.layers.trails = kmlLayer;
            
            var options = getElementsByTagAndClassName("input", "layer");
            forEach(options,
                    function(option) {
                        connect(option, 'onclick', function(evt) {
                            self.events.signal(Portal, 'toggleLayer');
                         });
                    });
            
            
            var options = getElementsByTagAndClassName("input", "infrastructure_option");
            forEach(options,
                    function(option) {
                        connect(option, 'onclick', function(evt) {
                            self.events.signal(Portal, 'toggleFacet');
                         });
                    });
            
            var options = getElementsByTagAndClassName("input", "natural_features_option");
            forEach(options,
                    function(option) {
                        connect(option, 'onclick', function(evt) {
                            self.events.signal(Portal, 'toggleFacet');
                         });
                    });
            
            options = getElementsByTagAndClassName("input", "featured_option");
            forEach(options,
                    function(option) {
                        connect(option, 'onclick', function(evt) {
                            self.events.signal(Portal, 'toggleFacet');
                         });
                    });      

            self.locations = self.initMarkers("geocode", 0);          
         });
    }
}


var portalMapInstance = new Portal.Map();
/* eslint-disable security/detect-non-literal-fs-filename */

if (typeof Portal === 'undefined') {
    var Portal = {};
}

if (!Portal.Base) {
    Portal.Base = {
        'Observer': function() {
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
                for (var a in _named_listeners) {
                    if (Object.prototype.hasOwnProperty.call(
                        _named_listeners, a)) {
                        this.removeListener(a);
                    }
                }
                for (var b in _listeners) {
                    if (Object.prototype.hasOwnProperty.call(_listeners, b)) {
                        this.removeListener(b);
                    }
                }
            };
            this.events = {
                signal: Portal.Base.Events.signal,
                connect: Portal.Base.Events.connect
            };
        } // Observer
    };
}

if (!Portal.Base.Events) {
    if (typeof MochiKit !== 'undefined') {
        Portal.Base.Events = {
            'connect': function(subject, event, self, func) {
                if (typeof subject.nodeType !== 'undefined' ||
                    subject === window ||
                    subject === document) {
                    event = 'on' + event;
                }
                var disc =
                    MochiKit.Signal.connect(subject, event, self, func);
                return {
                    disconnect: function() {
                        MochiKit.Signal.disconnect(disc);
                    }
                };
            },
            'signal': function(subject, event, param) {
                MochiKit.Signal.signal(subject, event, param);
            }
        };
    } else if (typeof jQuery !== 'undefined') {
        Portal.Base.Events = {
            'connect': function(subject, event, self, func) {
                var disc = jQuery(subject).bind(event, function() {
                    func.call(self, event, this);
                });
                return {
                    disconnect: function() {
                        disc.unbind(event);
                    }
                };
            },
            'signal': function(subject, event) {
                jQuery(subject).trigger(event);
            }
        };
    } else {
        throw Error('Use a framework');
    }
}

if (!Portal.Layer) {
    Portal.Layer = function(identifier, fileName, clickable) {
        var self = this;
        Portal.Base.Observer.apply(this, arguments); // inherit events

        self.identifier = identifier;

        var myOptions = {
            preserveViewport: 'true',
            suppressInfoWindows: true,
            clickable: clickable
        };
        self.instance = new google.maps.KmlLayer(fileName, myOptions);

        google.maps.event.addListener(self.instance, 'click',
            function(kmlEvent) {
                self.events.signal(Portal, 'kmlClicked', kmlEvent);
            });

        this.isVisible = function() {
            return self.instance.map !== null &&
                self.instance.map !== undefined;
        };

        this.shouldBeVisible = function() {
            var element = document.getElementById(self.identifier);
            return element.checked;
        };
    };
}

if (!Portal.MapMarker) {
    Portal.MapMarker = function() {
        var self = this;

        Portal.Base.Observer.apply(this, arguments); // inherit events
        self.assetIdentifier = null;
        self.description = null;
        self.featured = [];
        self.infrastructure = [];
        self.marker = null;
        self.latlng = null;

        this.create = function(mapInstance, assetIdentifier, name,
            description, lat, lng, featured,
            infrastructure, iconName, zIndex) {

            self.assetIdentifier = assetIdentifier;
            self.description = description;
            self.featured = featured;
            self.infrastructure = infrastructure;

            if (!lat || !lng) {
                return null;
            }

            var iconUrl = '';
            if (infrastructure && infrastructure.length) {
                var infraIcon = infrastructure[0];
                infraIcon = infraIcon.replace(/ /g, '');
                infraIcon = infraIcon.replace('-', '');
                iconUrl = STATIC_URL + 'images/portal/mapicon_' +
                    infraIcon.toLowerCase() + '.png';
            } else if (featured && featured.length) {
                var featuredIcon = featured[0];
                featuredIcon = featuredIcon.replace('Featured ', '');
                iconUrl = STATIC_URL + 'images/portal/mapicon_' +
                        featuredIcon.toLowerCase() + '.png';
            } else if (iconName) {
                if (iconName.indexOf('https:') === 0) {
                    iconUrl = iconName;
                } else {
                    iconUrl = STATIC_URL + 'images/portal/' +
                        iconName;
                }
            } else {
                iconUrl = STATIC_URL + 'images/portal/mapicon_main.png';
            }

            self.latlng = new google.maps.LatLng(lat, lng);
            var shouldBeVisible = self.shouldBeVisible();
            self.marker = new google.maps.Marker({
                position: self.latlng,
                title: name,
                icon: iconUrl,
                map: shouldBeVisible ? mapInstance: null,
                zIndex: zIndex
            });

            google.maps.event.addListener(self.marker, 'click', function() {
                self.events.signal(Portal, 'markerClicked',
                    self.assetIdentifier);
            });

            return self.latlng;
        };

        this.isVisible = function() {
            return self.marker.map !== null &&
                self.marker.map !== undefined;
        };

        this.shouldBeVisible = function() {
            var visible = false;
            var options = null;
            var values = null;

            if (self.infrastructure && self.infrastructure.length) {
                options = getElementsByTagAndClassName('input',
                    'infrastructure_option');
                values = self.infrastructure;
            } else if (self.featured && self.featured.length) {
                options = getElementsByTagAndClassName('input',
                    'featured_option');
                values = self.featured;
            } else {
                visible = true;
            }

            if (options) {
                forEach(options, function(option) {
                    if (option.checked) {
                        for (var i = 0; i < values.length; i++) {
                            if (option.value === values[i]) {
                                visible = true;
                            }
                        }
                    }
                });
            }

            return visible;
        };
    };
}

if (!Portal.Map) {
    Portal.Map = function() {
        var self = this;

        Portal.Base.Observer.apply(this, arguments); // inherit events

        self.mapInstance = null;
        self.locations = {};
        self.search_results = {};
        self.infoWindow = null;
        self.layers = {};

        this.hideInfoWindow = function() {
            if (self.infowindow) {
                self.infowindow.close();
            }
        };

        this.showLayerInfoWindow = function(kmlEvent) {
            if (self.infowindow) {
                self.infowindow.close();
            }

            var description;

            // @todo -- client-side templates?
            if (kmlEvent.featureData.name) {
                description =
                    '<div class="callout">' +
                    '<span class="callout-display-name">' +
                    kmlEvent.featureData.name + '</span>';
                if (kmlEvent.featureData.description) {
                    description += '<div class="callout-asset-types">' +
                        kmlEvent.featureData.description + '</div>';
                }
                description +=
                    '<a class="callout-summary-link" ' +
                    'onclick="portalMapInstance.search(' +
                    kmlEvent.latLng.lat() + ', ' +
                    kmlEvent.latLng.lng() +
                    ', \'' + escape(kmlEvent.featureData.name) +
                    '\')">Search nearby</a></div>';
            } else if (kmlEvent.featureData.description) {
                var title = kmlEvent.featureData.description.replace(
                    '_blank', '_self');
                description = '<div class="callout"><div>' +
                    title + '</div><br />';
                title = title.replace(/(<([^>]+)>)/ig, '');
                description +=
                    '<a class="callout-summary-link" ' +
                    'onclick="portalMapInstance.search(' +
                    kmlEvent.latLng.lat() + ', ' + kmlEvent.latLng.lng() +
                    ', \'' + escape(title) + '\')">Search nearby</a></div>';
            } else {
                description = kmlEvent.latLng.lat() +
                    ', ' + kmlEvent.latLng.lng();
            }

            var params = {
                content: description,
                position: kmlEvent.latLng,
                maxWidth: 400
            };
            if (kmlEvent.pixelOffset.height < 0) {
                params.pixelOffset = new google.maps.Size(-5, -20);
            }
            self.infowindow = new google.maps.InfoWindow(params);
            self.infowindow.open(self.mapInstance);
        };

        this.showMarkerInfoWindow = function(asset_identifier) {
            var location = self.locations[asset_identifier];
            if (!location) {
                location = self.search_results[asset_identifier];
            }

            if (!location && self.selected) {
                location = self.selected[asset_identifier];
            }

            if (location) {

                if (self.infowindow) {
                    self.infowindow.close();
                }

                var offset = new google.maps.Size(-5, 15);

                self.infowindow = new google.maps.InfoWindow({
                    content: location.description,
                    maxWidth: 400,
                    pixelOffset: offset
                });
                self.infowindow.open(self.mapInstance, location.marker);
            }
        };

        this.toggleFacet = function() {
            for (var assetIdentifier in self.locations) {
                if (Object.prototype.hasOwnProperty.call(self.locations,
                    assetIdentifier)) {
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
        };

        this.toggleLayer = function() {
            for (var identifier in self.layers) {
                if (Object.prototype.hasOwnProperty.call(self.layers,
                    identifier)) {
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
        };

        this.initMarkers = function(className, zIndexBoost, fitBounds) {
            // iterate over locations within the page,
            // and add the requested markers
            var bounds = new google.maps.LatLngBounds();
            var a = {};
            var elements = getElementsByTagAndClassName('div', className);
            var zIndex = 100 + zIndexBoost;
            forEach(elements, function(elem) {
                var assetIdentifier = getFirstElementByTagAndClassName(
                    null, 'asset_identifier', elem).value;
                var name = document.getElementById(assetIdentifier +
                    '-name').value;
                var description = document.getElementById(assetIdentifier +
                    '-description').innerHTML;
                var latitude = document.getElementById(assetIdentifier +
                    '-latitude').value;
                var longitude = document.getElementById(assetIdentifier +
                    '-longitude').value;

                var iconname = null;
                var property = document.getElementById(assetIdentifier +
                    '-iconname');
                if (property && property.value.length > 0) {
                    iconname = property.value;
                }

                var featured = null;
                var infrastructure = null;

                property = document.getElementById(assetIdentifier +
                    '-infrastructure');
                if (property && property.value.length > 0) {
                    infrastructure = property.value.split(',');
                }

                property = document.getElementById(assetIdentifier +
                    '-featured');
                if (property && property.value.length > 0) {
                    featured = property.value.split(',');
                }

                var marker = new Portal.MapMarker();
                var latlng = marker.create(self.mapInstance,
                    assetIdentifier, name, description, latitude,
                    longitude, featured, infrastructure, iconname,
                    zIndex);

                a[assetIdentifier] = marker;
                bounds.extend(latlng);
                zIndex--;
            });

            if (!bounds.isEmpty() && fitBounds) {
                // Don't zoom in too far on only one marker
                // http://stackoverflow.com/questions/3334729/
                // google-maps-v3-fitbounds-zoom-too-close-for-single-marker
                if (bounds.getNorthEast().equals(bounds.getSouthWest())) {
                    var extendPoint1 = new google.maps.LatLng(
                        bounds.getNorthEast().lat() + 0.01,
                        bounds.getNorthEast().lng() + 0.01);
                    var extendPoint2 = new google.maps.LatLng(
                        bounds.getNorthEast().lat() - 0.01,
                        bounds.getNorthEast().lng() - 0.01);
                    bounds.extend(extendPoint1);
                    bounds.extend(extendPoint2);
                }
                self.mapInstance.fitBounds(bounds);
            }

            return a;
        };

        this.search = function(lat, long, title) {
            for (var result in self.search_results) {
                if (Object.prototype.hasOwnProperty.call(self.search_results,
                    result)) {
                    var location = self.search_results[result];
                    location.marker.setMap(null);
                }
            }
            self.search_results = {};

            document.getElementById('map_filters').style.display = 'none';

            var nearby_results = document.getElementById('nearby_results');

            jQuery(nearby_results).show('fast', function() {
                var url = '/portal/nearby/' + lat + '/' + long + '/';
                var request = doXHR(url);
                request.addCallback(function(response) {
                    nearby_results.innerHTML = response.responseText;
                    document.getElementById('nearby_asset').innerHTML =
                        unescape(title);
                    self.search_results =
                        self.initMarkers('nearby', 0, true);

                    google.maps.event.addListenerOnce(
                        self.mapInstance,
                        'idle',
                        function() {
                            var center = new google.maps.LatLng(
                                lat,
                                long);
                            self.mapInstance.setCenter(center);
                        });

                });
            });
        };

        this.closeSearch = function() {
            document.getElementById('map_filters').style.display = 'block';
            var nearby_results = document.getElementById('nearby_results');
            nearby_results.innerHTML = '';
            nearby_results.style.display = 'none';

            for (var result in self.search_results) {
                if (Object.prototype.hasOwnProperty.call(self.search_results,
                    result)) {
                    var location = self.search_results[result];
                    location.marker.setMap(null);
                }
            }
            self.search_results = {};
            self.center();
        };

        this.center = function() {
            var latlng = new google.maps.LatLng(41.397459, -74.021848);
            self.mapInstance.setCenter(latlng);
            self.mapInstance.setZoom(13);
        };

        this.markerCount = function(myobj) {
            var count = 0;
            for (var k in myobj) {
                if (Object.prototype.hasOwnProperty.call(myobj, k)) {
                    count++;
                }
            }
            return count;
        };

        this.init = function() {
            if (!document.getElementById('map_canvas')) {
                return;
            }

            // Center on Black Rock Forest
            var latlng = new google.maps.LatLng(41.397459, -74.021848);
            var myOptions = {
                zoom: 13,
                center: latlng,
                mapTypeId: google.maps.MapTypeId.TERRAIN
            };

            var elt = document.getElementById('map_canvas');
            self.mapInstance = new google.maps.Map(elt, myOptions);

            self.events.connect(Portal, 'markerClicked', self,
                'showMarkerInfoWindow');
            self.events.connect(Portal, 'kmlClicked', self,
                'showLayerInfoWindow');
            self.events.connect(Portal, 'toggleFacet', self, 'toggleFacet');
            self.events.connect(Portal, 'toggleLayer', self, 'toggleLayer');

            var randomnumber = Math.floor(Math.random() * 100000);
            var options = getElementsByTagAndClassName('input', 'layer');
            forEach(options, function(option) {
                var kmllayer = new Portal.Layer(option.id,
                    STATIC_URL + 'kml/portal/' +
                    option.id + '.kml?version=' + randomnumber, true);
                self.layers[option.id] = kmllayer;

                connect(option, 'onclick', function(evt) {
                    self.events.signal(Portal, 'toggleLayer');
                });
            });

            options = getElementsByTagAndClassName('input', 'facet');
            forEach(options, function(option) {
                connect(option, 'onclick', function(evt) {
                    self.events.signal(Portal, 'toggleFacet');
                });
            });

            self.locations = self.initMarkers('geocode', 0, false);
            var detail_locations = self.initMarkers(
                'geocode_detail', 0, true);
            for (var key in detail_locations) {
                if (Object.prototype.hasOwnProperty.call(detail_locations,
                    key)) {
                    self.locations[key] = detail_locations[key];
                }
            }

            self.selected = self.initMarkers('geoselected', 0, true);
            if (self.markerCount(self.selected)) {
                google.maps.event.addListenerOnce(
                    self.mapInstance, 'idle', function() {
                        self.mapInstance.setZoom(14);

                        for (var s in self.selected) {
                            if (Object.prototype.hasOwnProperty.call(
                                self.selected, s)) {
                                self.showMarkerInfoWindow(s);
                            }
                        }
                    });
            }

            var url_base = STATIC_URL +
                'kml/portal/brfboundary.kml?newcachebuster=';

            var boundary = new Portal.Layer(
                'brfboundary', url_base + randomnumber, false);
            boundary.instance.setMap(self.mapInstance);

            self.toggleLayer();
        };
    };
}

var portalMapInstance = null;
addLoadEvent(function() {
    portalMapInstance = new Portal.Map();
    portalMapInstance.init();
});

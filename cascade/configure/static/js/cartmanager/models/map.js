/**
 *
 * User: jbennett
 * Date: 3/3/13
 * Time: 9:43 PM
 *
 */

(function (cartlogic) {

    function MapStyle() {

        var self = this;

        self.style = [
            {
                "featureType":"road.highway",
                "elementType":"geometry.fill",
                "stylers":[
                    { "color":"#636363" },
                    { "weight":2.5 }
                ]
            },
            {
                "featureType":"road.highway",
                "elementType":"geometry.stroke",
                "stylers":[
                    { "color":"#ffffff" },
                    { "weight":0.7 }
                ]
            },
            {
                "featureType":"road",
                "elementType":"labels.text.fill",
                "stylers":[
                    { "color":"#000000" },
                    { "weight":0.9 }
                ]
            },
            {
                "featureType":"road.local",
                "elementType":"labels.text",
                "stylers":[
                    { "color":"#000000" },
                    { "visibility":"on" },
                    { "weight":1.2 }
                ]
            },
            {
                "featureType":"road.arterial",
                "elementType":"labels.text.fill",
                "stylers":[
                    { "weight":0.8 },
                    { "color":"#000000" }
                ]
            },
            {
                "featureType":"road.local",
                "elementType":"labels.text.stroke",
                "stylers":[
                    { "color":"#A6E1F8" },
                    { "visibility":"on" },
                    { "weight":4.4 }
                ]
            },
            {
                "featureType":"road.arterial",
                "elementType":"geometry",
                "stylers":[
                    { "color":"#808080" },
                    { "weight":0.7 }
                ]
            },
            {
                "featureType":"road.arterial",
                "elementType":"labels.text",
                "stylers":[
                    { "color":"#ffffff" }
                ]
            },
            {
                "featureType":"road.arterial",
                "elementType":"labels.text.fill",
                "stylers":[
                    { "weight":0.8 },
                    { "color":"#000000" }
                ]
            },
            {
                "featureType":"road.highway",
                "elementType":"labels.text.stroke",
                "stylers":[
                    { "color":"#ffffff" },
                    { "weight":6.2 }
                ]
            },
            {
                "featureType":"road.local",
                "elementType":"geometry.fill",
                "stylers":[
                    { "color":"#ffffff" },
                    { "weight":3.5 }
                ]
            },
            {
                "featureType":"road.local",
                "elementType":"geometry",
                "stylers":[
                    { "color":"#ffffff" },
                    { "weight":1.3 }
                ]
            }
        ];

        self.getStyle = function () {
            return self.style;
        }
    }

  cartlogic.MapStyle = MapStyle;


 function GeocodeMap(element, lat_element, lon_element, status_element, options) {
        var self = this;

         console.log(options.address);

         self.geocode = function () {
            //Planning to add other client geocoders in the future this is a reminder of where to do it

            if (options.coder == 'google') {
               geocoder = new google.maps.Geocoder();

               geocoder.geocode({'address':options.address}, function (results, status) {
                    if (status == google.maps.GeocoderStatus.OK) {
                        var lat = results[0].geometry.location.lat();
                        var lon = results[0].geometry.location.lng();

                         $("#map_address_wrapper").html('<img src="https://maps.googleapis.com/maps/api/staticmap?center='+ lat+','+lon +'&zoom=16&size=600x275&maptype=roadmap&markers' +
                            '=color:blue%7Clabel:*%7C' +lat + ',' + lon + '&style='+'&sensor=false" />');

                            $("#" + lat_element).val(lat);
                            $("#" + lon_element).val(lon);
                            $("#" + status_element).val(results[0].geometry.location_type);

                    } else {
                        element.innerHTML = "Geocode was not successful for the following reason: " + status;
                    }
                });
            }
        }
    }

    cartlogic.GeocodeMap = GeocodeMap;


    function Marker(type, info) {
        var self = this;

        if (type == 'cart') {
            var image = new google.maps.MarkerImage(
                static_url + 'img/marker-images/image.png',
                new google.maps.Size(40, 50),
                new google.maps.Point(0, 0),
                new google.maps.Point(20, 50)
            );

            var shadow = new google.maps.MarkerImage(
                static_url + 'img/marker-images/shadow.png',
                new google.maps.Size(68, 50),
                new google.maps.Point(0, 0),
                new google.maps.Point(20, 50)
            );

            var shape = {
                coord:[35, 4, 36, 5, 37, 6, 37, 7, 36, 8, 35, 9, 35, 10, 35, 11, 35, 12, 35, 13, 35, 14, 35, 15, 35, 16,
                    35, 17, 34, 18, 34, 19, 34, 20, 34, 21, 34, 22, 34, 23, 34, 24, 34, 25, 34, 26, 34, 27, 33, 28,
                    33, 29, 33, 30, 33, 31, 33, 32, 33, 33, 33, 34, 33, 35, 33, 36, 33, 37, 33, 38, 33, 39, 33, 40,
                    33, 41, 33, 42, 33, 43, 29, 44, 28, 45, 27, 46, 27, 47, 19, 47, 16, 46, 13, 45, 8, 44, 7, 43, 6,
                    42, 5, 41, 5, 40, 5, 39, 5, 38, 5, 37, 6, 36, 8, 35, 10, 34, 10, 33, 10, 32, 9, 31, 9, 30, 9, 29,
                    9, 28, 9, 27, 9, 26, 9, 25, 9, 24, 9, 23, 9, 22, 8, 21, 8, 20, 7, 19, 5, 18, 5, 17, 5, 16, 5, 15,
                    5, 14, 4, 13, 4, 12, 4, 11, 4, 10, 3, 9, 3, 8, 3, 7, 2, 6, 6, 5, 15, 4, 35, 4],
                type:'poly'
            };
        }


        self.marker = new google.maps.Marker({
            draggable:true,
            raiseOnDrag:true,
            icon:image,
            shadow:shadow,
            shape:shape,
            title:info
        });


        self.getMarker = function () {
            return self.marker;
        }

    }

    cartlogic.Marker = Marker;

/*
   Removed in favor of putting maps in the ViewModels
    function SingleCartMap(element, options) {


        var self = this;

        if (options.lat && options.lon) {

            self.cartLatLng = new google.maps.LatLng(options.lat, options.lon);
            self.style = new cartlogic.MapStyle();
            self.marker = new cartlogic.Marker('cart', options.label).getMarker();


            self.mapOptions = {
                center:self.cartLatLng,
                zoom:15,
                mapTypeId:google.maps.MapTypeId.ROADMAP,
                styles:self.style.getStyle()
            };

            var map = new google.maps.Map(element, self.mapOptions);
            console.log("in single map")
            google.maps.event.trigger(map, 'resize');

            self.marker.setPosition(self.cartLatLng);
            self.marker.setMap(map);


            google.maps.event.addListener(self.marker, 'dragend', function () {
                self.updateCoordinates();
            });


        }
    }

    cartlogic.SingleCartMap = SingleCartMap;
*/

})(window.cartlogic);

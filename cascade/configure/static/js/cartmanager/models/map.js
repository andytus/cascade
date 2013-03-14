/**
 *
 * User: jbennett
 * Date: 3/3/13
 * Time: 9:43 PM
 *
 */

(function (cartlogic){

        function Map(element, info, lat, lon){

            var style = [
                {
                    "featureType": "road.highway",
                    "elementType": "geometry.fill",
                    "stylers": [
                        { "color": "#636363" },
                        { "weight": 2.5 }
                    ]
                },{
                    "featureType": "road.highway",
                    "elementType": "geometry.stroke",
                    "stylers": [
                        { "color": "#ffffff" },
                        { "weight": 0.7 }
                    ]
                },{
                    "featureType": "road",
                    "elementType": "labels.text.fill",
                    "stylers": [
                        { "color": "#000000" },
                        { "weight": 0.9 }
                    ]
                },{
                    "featureType": "road.local",
                    "elementType": "labels.text",
                    "stylers": [
                        { "color": "#000000" },
                        { "visibility": "on" },
                        { "weight": 1.2 }
                    ]
                },{
                    "featureType": "road.arterial",
                    "elementType": "labels.text.fill",
                    "stylers": [
                        { "weight": 0.8 },
                        { "color": "#000000" }
                    ]
                },{
                    "featureType": "road.local",
                    "elementType": "labels.text.stroke",
                    "stylers": [
                        { "color": "#A6E1F8" },
                        { "visibility": "on" },
                        { "weight": 4.4 }
                    ]
                },{
                    "featureType": "road.arterial",
                    "elementType": "geometry",
                    "stylers": [
                        { "color": "#808080" },
                        { "weight": 0.7 }
                    ]
                },{
                    "featureType": "road.arterial",
                    "elementType": "labels.text",
                    "stylers": [
                        { "color": "#ffffff" }
                    ]
                },{
                    "featureType": "road.arterial",
                    "elementType": "labels.text.fill",
                    "stylers": [
                        { "weight": 0.8 },
                        { "color": "#000000" }
                    ]
                },{
                    "featureType": "road.highway",
                    "elementType": "labels.text.stroke",
                    "stylers": [
                        { "color": "#ffffff" },
                        { "weight": 6.2 }
                    ]
                },{
                    "featureType": "road.local",
                    "elementType": "geometry.fill",
                    "stylers": [
                        { "color": "#ffffff" },
                        { "weight": 3.5 }
                    ]
                },{
                    "featureType": "road.local",
                    "elementType": "geometry",
                    "stylers": [
                        { "color": "#ffffff" },
                        { "weight": 1.3 }
                    ]
                }
            ];

            var cartLatlng = new google.maps.LatLng(lat, lon);
            var mapOptions = {
                center: cartLatlng,
                zoom: 15,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                styles: style
            };
            var map = new google.maps.Map(element,
                mapOptions);


            var image = new google.maps.MarkerImage(
                static_url + 'img/marker-images/image.png',
                new google.maps.Size(40,50),
                new google.maps.Point(0,0),
                new google.maps.Point(20,50)
            );

            var shadow = new google.maps.MarkerImage(
                static_url +'img/marker-images/shadow.png',
                new google.maps.Size(68,50),
                new google.maps.Point(0,0),
                new google.maps.Point(20,50)
            );

            var shape = {
                coord: [35,4,36,5,37,6,37,7,36,8,35,9,35,10,35,11,35,12,35,13,35,14,35,15,35,16,35,17,34,18,34,19,34,20,34,21,34,22,34,23,34,24,34,25,34,26,34,27,33,28,33,29,33,30,33,31,33,32,33,33,33,34,33,35,33,36,33,37,33,38,33,39,33,40,33,41,33,42,33,43,29,44,28,45,27,46,27,47,19,47,16,46,13,45,8,44,7,43,6,42,5,41,5,40,5,39,5,38,5,37,6,36,8,35,10,34,10,33,10,32,9,31,9,30,9,29,9,28,9,27,9,26,9,25,9,24,9,23,9,22,8,21,8,20,7,19,5,18,5,17,5,16,5,15,5,14,4,13,4,12,4,11,4,10,3,9,3,8,3,7,2,6,6,5,15,4,35,4],
                type: 'poly'
            };


            var marker = new google.maps.Marker({
                draggable: true,
                raiseOnDrag: true,
                icon: image,
                shadow: shadow,
                shape: shape,
                position: cartLatlng,
                map: map,
                title: info
            });


            google.maps.event.addListener(marker, 'dragend', function() {
                console.log(marker.getPosition().lat());
                self.updateCoordinates();
            });


        }

    cartlogic.Map = Map;

})(window.cartlogic);

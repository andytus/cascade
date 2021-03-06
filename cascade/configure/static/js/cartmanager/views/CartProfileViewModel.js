/**
 *
 * User: jbennett
 * Date: 2/27/13
 * Time: 7:51 PM
 *
 */


(function (cartlogic) {


    function CartProfileViewModel() {

        var self = this;
        self.cart = ko.observable();
        //Adding cart id to root for a hack (bad practice should be able to get from root.profile.cart.id, but doing this for now.
        self.cart_id = ko.observable();
        self.cart_status_options = ko.observableArray([]);
        self.cart_type_options = ko.observableArray([]);

        self.getCartData = function () {
            $.ajax({
                url:cart_api_profile + cart_serial_number,
                type:"GET",
                dataType:"json",
                success:function (data) {
                    self.cart(new cartlogic.CartProfile(data));
                    self.cart_id(self.cart().id());
                    //Calling to get cart type options for this cart
                    //filters based on size and needs to get the size from the current cart size
                    self.getTypeOptions();
                    //Calling to get the cart status options
                    self.getStatusOptions();
                    //Change data going into the new ticket link tool bar
                    $("#new-ticket-link").attr("href", ticket_app_new + 'New?cart_id=' + data.id);
                },
                error:function (data) {
                    $("#message").removeClass("alert-info").addClass("alert-error").html("Error:" + data.statusText).show();
                }

            });

        };

        self.getStatusOptions = function () {
            $.getJSON(cart_status_options_api_url + "?format=jsonp&callback=?", function (data) {
                var cartStatusOptions = $.map(data, function (item) {
                    return new cartlogic.CartStatusOptions(item);
                });
                self.cart_status_options(cartStatusOptions);
                //set drop down to current status
                $("#cart-info-edit-status option[value='" + self.cart().current_status_id() + "']").attr("selected", "selected");
            })
        };

        self.getTypeOptions = function () {
            url = cart_type_options_api_url + "?format=jsonp&callback=?";
            data = {'size':self.cart().cart_type__size()};
            $.getJSON(url, data, function (data) {
                var cartTypeOptions = $.map(data, function (item) {
                    return new cartlogic.CartTypeOption(item)
                });
                self.cart_type_options(cartTypeOptions);
                //Set drop down to current cart type
                $("#cart-info-edit-type option[value='" + self.cart().cart_type__name() + "']").attr("selected", "selected");
            })
        };

        self.setCartInfo = function () {
            //need to find current level for correct labeling
            var type = $('#cart-info-edit-type option:selected').text();
            self.cart().cart_type__name(type);

            var status = $("#cart-info-edit-status option:selected");
            self.cart().current_status(status.text());
            level = self.cart_type_options();
            var match = ko.utils.arrayFirst(self.cart_status_options(), function (item) {
                return status.val() == item.id();
            });

            self.cart().current_status_level(match.level())

        };

        self.saveCartData = function (data) {
            $.ajax(cart_api_profile + cart_serial_number, {
                data:ko.toJSON(data),
                type:"post", contentType:"application/json",
                dataType:"jsonp",
                success:function (data) {
                    self.cart().last_updated(new Date(data.details.time).toDateString());
                    //refresh cart info on page
                    self.setCartInfo();
                    $("#message-type").text(data.details.message_type + "! ");
                    $("#message-text").text(data.details.message);
                    $('.close').click(function() {
                        $('#message').hide();
                    });
                    if (data.details.message_type == 'Success') {
                        $("#message").removeClass("alert-error").addClass('alert-success').show();
                    } else {
                        $("#message").removeClass("alert-success").addClass('alert-error').show();
                    }
                    document.location.href = '#message';
                    //Call get cart to refresh the cart model
                    // self.getCartData()
                },
                error:function (data) {
                    $("#message").addClass("alert-error").show();
                    $("#message-type").text("Error! ");
                    $("#message-text").text(data.statusText);
                    $('.close').click(function () {
                        $('#message').hide();
                    })
                }
            })


        };

        self.updateCartInfo = function(){
            self.cart().cart_type__name(document.getElementById('cart-info-edit-status').text);
            var data = {current_status:document.getElementById('cart-info-edit-status').value,
                        cart_type__name:document.getElementById('cart-info-edit-type').value,
                        cart_type__size: self.cart().cart_type__size()
                        };

            self.saveCartData(data);
        };


        self.createMap = function () {

            //check if the Map is hidden
            var isMapHidden = $("#cart-profile-map").is(':hidden');

            if (isMapHidden) {

                var locationLatLng = new google.maps.LatLng(self.cart().location_latitude(), self.cart().location_longitude());
                var cartLatLng;

                var style = new cartlogic.MapStyle();
                var cart_marker = new cartlogic.Marker('cart', self.cart().rfid()).getMarker();
                var location_marker = new cartlogic.Marker(self.cart().location_type(), self.cart().location_address()).getMarker();



                var mapOptions = {
                    zoom:15,
                    mapTypeId:google.maps.MapTypeId.ROADMAP,
                    styles:style.getStyle()
                };

                //Check for cart last_latitude and position map center to cart last location else position on customer location

                if (self.cart().last_latitude() != null) {
                    cartLatLng = new google.maps.LatLng(self.cart().last_latitude(), self.cart().last_longitude());
                    mapOptions.center = cartLatLng;

                } else {
                    //make the cart location the same as the customer location
                    cartLatLng = locationLatLng;
                    mapOptions.center = locationLatLng;
                }

                var map = new google.maps.Map(document.getElementById("cart-profile-map"), mapOptions);
                // google.maps.event.trigger(map, 'resize');
                location_marker.setPosition(locationLatLng);
                location_marker.setMap(map);

                cart_marker.setPosition(cartLatLng);
                cart_marker.setMap(map);


                google.maps.event.addListener(cart_marker, 'dragend', function (coord) {
                    //updating client last lat and long (must call updateCoordinates to set on server
                    var lat = coord.latLng.lat();
                    var lng = coord.latLng.lng();
                    $('#update_coordinates').modal('show');
                    $('#set_latitude').text(lat);
                    $('#set_longitude').text(lng);
                    self.cart().last_latitude(lat);
                    self.cart().last_longitude(lng);
                });

                $('#cart-map-wrapper').show();

            }

            document.location.href = '#cart-profile-map';
        };


        self.updateCoordinates = function () {
            $('#update_coordinates').modal('hide');
            self.saveCartData({latitude: self.cart().last_latitude, longitude:self.cart().last_longitude});
        };

        //call the api to get the data on load
        self.getCartData();


    }

    cartlogic.CartProfileViewModel = CartProfileViewModel;

})(window.cartlogic);

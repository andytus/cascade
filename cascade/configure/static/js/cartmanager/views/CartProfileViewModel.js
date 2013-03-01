/**
 *
 * User: jbennett
 * Date: 2/27/13
 * Time: 7:51 PM
 *
 */


/**
 * User: joe.bennett
 * Date: 12/22/12
 * Time: 12:16 AM
 * s.
 */



function Location(data) {
    this.id = ko.observable(data.id);
    this.house_number = ko.observable(data.house_number);
    this.street_name = ko.observable(data.street_name);
}

function StatusOption(data) {
    this.id = ko.observable(data.id);
    this.level = ko.observable(data.level);
    this.label = ko.observable(data.label);
}

function TypeOption(data) {
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
    this.size = ko.observable(data.size);
    this.site = ko.observable(data.site);
}


(function (cartlogic){


function CartProfileViewModel() {

    var self = this;

    self.cart = ko.observable();
    self.cart_status_options = ko.observableArray([]);
    self.cart_type_options = ko.observableArray([]);

    self.changeCartStatus = ko.computed(function() {
        //#TODO Got to be a cleaner way
        $('#cart-info-edit-status').change(function () {
            var status = $("#cart-info-edit-status option:selected");
            self.cart.current_status(status.text());
            level = self.cart_status_options();
            var match = ko.utils.arrayFirst(self.cart_status_options(), function (item) {
                return status.val() == item.id();
            });

            self.cart.current_status_level(match.level())

        });});

        //type information
    self.changeCartType = ko.computed(function() {
            $('#cart-info-edit-type').change(function () {
                var type = $('#cart-info-edit-type option:selected').text();
                self.cart.cart_type(type);
            })
        });


    self.getCartData = function () {
        $.getJSON(cart_api_url + serial_number, function (data) {
            var profile_cart = new cartlogic.CartProfile(data);
            self.cart(profile_cart);
            console.log(self.cart());
            //Calling to get cart type options for this cart
            //filters based on size and needs to get the size from the current cart size
            self.getTypeOptions();
            //Calling to get the cart status options
            self.getStatusOptions();
            self.map();
        });
    };

    self.getStatusOptions = function () {
        $.getJSON(cart_status_options_api_url + "?format=jsonp&callback=?", function (data) {
            var cartStatusOptions = $.map(data, function (item) {
                return new StatusOption(item);
            });
            self.cart_status_options(cartStatusOptions);
            //set drop down to current status
            $("#cart-info-edit-status option[value='" + self.current_status_id() + "']").attr("selected", "selected");
        })
    };

    self.getTypeOptions = function () {
        url = cart_type_options_api_url + "?format=jsonp&callback=?";
        console.log(self.cart.size());
        data = {'size':self.cart.size()};
        $.getJSON(url, data, function (data) {
            var cartTypeOptions = $.map(data, function (item) {
                return new TypeOption(item)
            });
            self.cart_type_options(cartTypeOptions);
            //Set drop down to current cart type
            $("#cart-info-edit-type option[value='" + self.cart_type_id() + "']").attr("selected", "selected");
        })
    };

    self.saveCartData = function () {
        $.ajax(cart_api_url + serial_number, {
            data:ko.toJSON({current_status:self.cart.current_status, cart_type:document.getElementById('cart-info-edit-type').value}),
            type:"post", contentType:"application/json",
            dataType:"jsonp",
            success:function (result) {
                self.last_updated(new Date(result.time).toDateString());
                $("#message").addClass("alert-success").show();
                $("#message-type").text("Success! ");
                $("#message-text").text(result.message);
                $('.close').click(function () {
                    $('#message').hide();
                });
                //Call get cart to refresh the cart model
                self.getCartData()
            },
            error:function (result) {
                //#TODO test this!
                $("#message").addClass("alert-warning").show();
                $("#message-type").text("Failed! ");
                $("#message-text").text(result.message.Description);
                $('.close').click(function () {
                    $('#message').hide();
                    //Call get cart to refresh the cart model

                })
            }
        })


    };

    self.map = function(){

        var cartLatlng = new google.maps.LatLng(self.cart.location_latitude(), self.cart.location_longitude());
        var mapOptions = {
            center: cartLatlng,
            zoom: 12,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        var map = new google.maps.Map(document.getElementById("map_canvas"),
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
            title: self.rfid()
        });

        google.maps.event.addListener(marker, 'dragend', function() {
            console.log(marker.getPosition().lat());
        });


    };

    self.getLocation = function () {

    };

    self.updateLocation = function () {

    };

    //call the api to get the data on load
    self.getCartData();
}

    cartlogic.CartProfileViewModel = CartProfileViewModel;

})(window.cartlogic);


/*
$(document).ready(function () {
        var cart_profile = ko.applyBindings(new CartProfileViewModel(), document.getElementById("cart_profile"));
        var tickets = ko.applyBindings(new TicketsModelView(), document.getElementById("ticket_panel"));
    }
);

*/


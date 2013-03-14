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




(function (cartlogic){


function CartProfileViewModel() {

    var self = this;
    self.cart = ko.observable();
    //Adding cart id to root for a hack (bad practice should be able to get from root.profile.cart.id, but doing this for now.
    self.cart_id = ko.observable();
    self.cart_status_options = ko.observableArray([]);
    self.cart_type_options = ko.observableArray([]);
    self.getCartData = function () {
        $.getJSON(cart_api_url + serial_number, function (data) {
            self.cart(new cartlogic.CartProfile(data));
            self.cart_id(self.cart().id());
             //Calling to get cart type options for this cart
            //filters based on size and needs to get the size from the current cart size
            self.getTypeOptions();
            //Calling to get the cart status options
            self.getStatusOptions();
            cartlogic.Map(document.getElementById("map_canvas"), self.cart().rfid(), self.cart().location_latitude(), self.cart().location_longitude());
        });
    };

    self.getStatusOptions = function () {
        $.getJSON(cart_status_options_api_url + "?format=jsonp&callback=?", function (data) {
            var cartStatusOptions = $.map(data, function (item) {
                return new cartlogic.StatusOption(item);
            });
            self.cart_status_options(cartStatusOptions);
            //set drop down to current status
            $("#cart-info-edit-status option[value='" + self.cart().current_status_id() + "']").attr("selected", "selected");
        })
    };

    self.getTypeOptions = function () {
        url = cart_type_options_api_url + "?format=jsonp&callback=?";
        data = {'size':self.cart().size()};
        $.getJSON(url, data, function (data) {
            var cartTypeOptions = $.map(data, function (item) {
                return new cartlogic.TypeOption(item)
            });
            self.cart_type_options(cartTypeOptions);
            //Set drop down to current cart type
            $("#cart-info-edit-type option[value='" + self.cart().cart_type_id() + "']").attr("selected", "selected");
        })
    };

    self.updateCartInfo = function(){
       // var status = document.getElementById('cart-info-edit-status');
       // self.cart().current_status(status.options[status.selectedIndex].text);
        //need to find current level for correct labeling
        var type = $('#cart-info-edit-type option:selected').text();
        self.cart().cart_type(type);

        var status = $("#cart-info-edit-status option:selected");
        self.cart().current_status(status.text());
        level = self.cart_type_options();
        var match = ko.utils.arrayFirst(self.cart_status_options(), function(item){
           return status.val() == item.id();
        });

        self.cart().current_status_level(match.level())

    };

    self.saveCartData = function () {
        self.cart().cart_type(document.getElementById('cart-info-edit-status').text);
        $.ajax(cart_api_url + serial_number, {
            data:ko.toJSON({current_status:document.getElementById('cart-info-edit-status').value, cart_type:document.getElementById('cart-info-edit-type').value}),
            type:"post", contentType:"application/json",
            dataType:"jsonp",
            success:function (result) {
                self.cart().last_updated(new Date(result.time).toDateString());
                self.updateCartInfo();
                $("#message").addClass("alert-success").show();
                $("#message-type").text("Success! ");
                $("#message-text").text(result.message);
                $('.close').click(function () {
                    $('#message').hide();
                });
                //Call get cart to refresh the cart model
               // self.getCartData()
            },
            error:function (result) {
                //#TODO test this!
                console.log("fail");
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

   self.mapExpand = function(){
       //#TODO

       // window.open(cart_app_profile_map + serial_number);

    };


    self.getLocation = function () {
        //#TODO

    };

    self.updateLocation = function () {
        //#TODO

    };

    self.updateCoordinates = function(){
        console.log("updateCoordinates")
    };

    //call the api to get the data on load


    self.getCartData();

}

    cartlogic.CartProfileViewModel = CartProfileViewModel;

})(window.cartlogic);

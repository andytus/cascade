/**
 *
 * User: jbennett
 * Date: 2/27/13
 * Time: 7:50 PM
 *
 */


(function (cartlogic){

function CartProfile(data){

    var self = this;

    self.last_longitude = ko.observable(data.last_longitude);
    self.last_latitude = ko.observable(data.last_latitude);
    self.rfid = ko.observable(data.rfid);
    self.serial_number = ko.observable(data.serial_number);

    self.id = ko.observable(data.id);
    self.cart_profile_url = ko.observable(data.cart_url);
    self.size = ko.observable(data.cart_type.size);
    self.cart_type = ko.observable(data.cart_type.name);
    self.cart_type_id = ko.observable(data.cart_type.id);
    self.last_updated = ko.observable(new Date(data.last_updated).toDateString());
    self.born_date = ko.observable(new Date(data.born_date).toDateString());
    //location information
    self.location_house_number = ko.observable(data.location.house_number);
    self.location_street_name = ko.observable(data.location.street_name);
    self.location_unit = ko.observable(data.location.unit);
    self.location_address = ko.computed(function () {
        address = self.location_house_number() + " " + self.location_street_name();
        if (self.location_unit()) {
            address = address + " Unit: " + self.location_unit();
        }
        return address
    });

    self.location_latitude = ko.observable(data.location.latitude);
    self.location_longitude = ko.observable(data.location.longitude);
    self.location_type = ko.observable(data.location.type);

    //customer information
    self.customer_id = ko.observable(data.location.customer.info.id);
    self.customer_name = ko.observable(data.location.customer.info.name);
    self.customer_url = ko.observable(data.location.customer.info.url);


    //status information
    self.current_status_id = ko.observable(data.current_status.id);
    self.current_status = ko.observable(data.current_status.id.label);
    self.current_status_level = ko.observable(data.current_status.id.level);

/*    self.cart_status_options = ko.observableArray([]);
    self.cart_type_options = ko.observableArray([]);


    self.changeCartStatus = ko.computed(function () {
        //#TODO Got to be a cleaner way
        $('#cart-info-edit-status').change(function () {
            var status = $("#cart-info-edit-status option:selected");
            self.current_status(status.text());
            level = self.cart_status_options();
            var match = ko.utils.arrayFirst(self.cart_status_options(), function (item) {
                return status.val() == item.id();
            });

            self.current_status_level(match.level())

        });

        //type information

        self.changeCartType = ko.computed(function () {
            $('#cart-info-edit-type').change(function () {
                var type = $('#cart-info-edit-type option:selected').text();
                self.cart_type(type);
            })
        });

    });*/
}

cartlogic.CartProfile = CartProfile;

}(window.cartlogic));
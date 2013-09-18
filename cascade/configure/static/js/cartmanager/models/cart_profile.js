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
    self.cart_type__size = ko.observable(data.cart_type.size);
    self.cart_type__name = ko.observable(data.cart_type.name);
    self.cart_type__id = ko.observable(data.cart_type.id);

    self.last_updated = ko.observable(new cartlogic.DateFormat(data.last_updated).full_date);

    if(data.born_date != null){
        self.born_date = ko.observable(new cartlogic.DateFormat(data.born_date).full_date);
    } else{
        self.born_date = ko.observable("Unknown")
    }


    //location information
    if(data.location != null){

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

    } else{
    self.location_house_number = ko.observable(null);
    self.location_street_name = ko.observable(null);
    self.location_unit = ko.observable(null);
    self.location_address = ko.observable(null);
    }


    if(data.location != null && data.location.customer != null){
    //customer information
    self.customer_id = ko.observable(data.location.customer.info.id);
    self.customer_name = ko.observable(data.location.customer.info.name);
    self.customer_url = ko.observable(data.location.customer.info.url);
    } else{
    self.customer_id = ko.observable(null);
    self.customer_name = ko.observable("Add or Change Customer");
    self.customer_url = ko.observable(null);
    }


    //status information
    self.current_status_id = ko.observable(data.current_status.id);
    self.current_status = ko.observable(data.current_status.label);
    self.current_status_level = ko.observable(data.current_status.level);

}

cartlogic.CartProfile = CartProfile;

}(window.cartlogic));
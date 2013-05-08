/**
 *
 * User: jbennett
 * Date: 2/28/13
 * Time: 9:02 AM
 *
 */

(function (cartlogic){


function Ticket(data) {
    var self = this;
    self.id = ko.observable();
    self.status = ko.observable();
    self.processed = ko.observable();
    self.status_level = ko.observable();
    self.service_type = ko.observable();
    self.success_attempts = ko.observable();
    self.date_created = ko.observable();
    self.date_last_attempted = ko.observable();
    self.date_completed = ko.observable("none");
    self.house_number = ko.observable();
    self.street_name = ko.observable();
    self.unit = ko.observable();
    self.serviced_cart = ko.observable();
    self.serviced_cart_id = ko.observable();
    self.serviced_cart_size = ko.observable();
    self.serviced_cart_type = ko.observable();
    self.expected_cart = ko.observable();
    self.cart_type = ko.observable();
    self.cart_type_size = ko.observable();
    self.latitude = ko.observable();
    self.longitude = ko.observable();
    self.device_name = ko.observable();
    self.created_by = ko.observable();
    self.updated_by = ko.observable();
    self.comments = ko.observable();

    if (data){
        self.id(data.id);
        self.status(data.status);
        self.processed(data.processed);
        self.status_level(data.status_level);
        self.service_type(data.service_type);
        self.success_attempts(data.success_attempts);
        self.date_created(new Date(data.date_created).toDateString());
        self.date_last_attempted(new Date(data.date_last_attempted).toDateString());
        if (data.completed){
            self.date_completed(new Date(data.date_completed).toDateString());
        }
        self.house_number(data.house_number);
        self.street_name(data.street_name);
        self.unit(data.unit);

        self.location_address = ko.computed(function () {
            address = self.house_number() + " " + self.street_name();
            if (self.unit()) {
                address = address + " Unit: " + self.unit();
            }
            return address
        });


        self.serviced_cart(data.serviced_cart);
        self.serviced_cart_id(data.serviced_cart_id);
        self.serviced_cart_size(data.serviced_cart_size);
        self.serviced_cart_type(data.serviced_cart_type);
        self.expected_cart(data.expected_cart);
        self.cart_type(data.cart_type);
        self.cart_type_size(data.cart_type_size);
        self.latitude(data.latitude);
        self.longitude(data.longitude);
        self.device_name(data.device_name);
        self.created_by(data.created_by);
        self.updated_by(data.updated_by);
    }

}
    cartlogic.Ticket = Ticket;

})(window.cartlogic);
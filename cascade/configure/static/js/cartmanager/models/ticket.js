/**
 *
 * User: Joe Bennett
 * Date: 2/28/13
 * Time: 9:02 AM
 *
 * Ticket Model
 *
 */

(function (cartlogic){


function Ticket(data) {
    var self = this;
    //core ticket attributes
    self.id = ko.observable();
    self.latitude = ko.observable();
    self.longitude = ko.observable();
    self.processed = ko.observable();
    self.device_name = ko.observable();
    self.success_attempts = ko.observable();
    self.date_created = ko.observable();
    self.date_last_attempted = ko.observable();
    self.date_completed = ko.observable("none");

    //status attributes, level used for css style
    self.status__service_status = ko.observable();
    self.status__level = ko.observable();
    self.reason_code__description = ko.observable();

    //location of ticket
    self.location__house_number = ko.observable();
    self.location__street_name = ko.observable();
    self.location__unit = ko.observable();
    self.location__customer__get_app_url = ko.observable();

    //serviced cart attributes
    self.serviced_cart__serial_number = ko.observable();
    self.serviced_cart__id = ko.observable();
    self.serviced_cart__cart_type__size = ko.observable();
    self.serviced_cart__cart_type__name = ko.observable();

    //service_type code (also available from JSON is service type service (i.e. Exchange Remove, Delivery, etc..)
    self.service_type__code = ko.observable();
    self.service_type__service = ko.observable();

    //expected cart serial number
    self.expected_cart__serial_number = ko.observable();

    //cart type for the ticket
    self.cart_type__name = ko.observable();
    self.cart_type__size = ko.observable();

    //user who created and last updated by
    self.created_by__username = ko.observable();
    self.updated_by__username = ko.observable();

    //one to many relationship
    self.comments = ko.observable(); //Are we using this?

    //loads data into attribute if available
    if (data){
        self.id(data.id);
        self.latitude(data.latitude);
        self.longitude(data.longitude);
        self.processed(data.processed);
        self.device_name(data.device_name);
        self.success_attempts(data.success_attempts);
        self.date_created(new cartlogic.DateFormat(data.date_created).full_date);
        self.date_last_attempted(new cartlogic.DateFormat(data.date_last_attempted).full_date);

        if (data.date_completed){
            self.date_completed(new cartlogic.DateFormat(data.date_completed).full_date);
        }

        self.status__service_status(data.status__service_status);
        self.status__level(data.status__level);
        self.reason_code__description(data.reason_code__description);


        self.location__house_number(data.location__house_number);
        self.location__street_name(data.location__street_name);
        self.location__unit(data.location__unit);
        self.location_address = ko.computed(function () {
            var address = self.location__house_number() + " " + self.location__street_name();
            if (self.location__unit()) {
                address = address + " Unit: " + self.location__unit();
            }
            return address;
        });
        self.location__customer__get_app_url(data.location__customer__get_app_url);

        self.serviced_cart__serial_number(data.serviced_cart__serial_number);
        self.serviced_cart__id(data.serviced_cart__id);
        self.serviced_cart__cart_type__size(data.serviced_cart__cart_type__size);
        self.serviced_cart__cart_type__name(data.serviced_cart__cart_type__name);


        self.service_type__code(data.service_type__code);
        self.service_type__service(data.service_type__service);

        self.expected_cart__serial_number(data.expected_cart__serial_number);


        self.cart_type__name(data.cart_type__name);
        self.cart_type__size(data.cart_type__size);

        self.created_by__username(data.created_by__username);
        self.updated_by__username(data.updated_by__username);

    }

}
    cartlogic.Ticket = Ticket;

})(window.cartlogic);
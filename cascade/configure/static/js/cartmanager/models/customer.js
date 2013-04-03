/**
 *
 * User: jbennett
 * Date: 3/23/13
 * Time: 11:13 AM
 *
 */


(function (cartlogic) {

    function Customer(data) {

        var self = this;
        self.customer_id = ko.observable(data.id);
        self.first_name = ko.observable(data.first_name);
        self.last_name = ko.observable(data.last_name);
        self.phone_number = ko.observable(data.phone_number);
        self.email = ko.observable(data.email);

    }


    cartlogic.Customer = Customer;

})(window.cartlogic);
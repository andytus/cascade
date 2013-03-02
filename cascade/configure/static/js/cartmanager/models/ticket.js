/**
 *
 * User: jbennett
 * Date: 2/28/13
 * Time: 9:02 AM
 *
 */

(function (cartlogic){


function Ticket(data) {
    this.status = ko.observable(data.status);
    this.service_type = ko.observable(data.service_type);
    this.success_attempts = ko.observable(data.success_attempts);
    this.date_created = (new Date(data.date_created).toDateString());
    this.date_last_attempted = ko.observable(new Date(data.date_last_attempted).toDateString());
    this.house_number = ko.observable(data.house_number);
    this.street_name = ko.observable(data.street_name);
    this.unit = ko.observable(data.unit);
    this.serviced_cart = ko.observable(data.serviced_cart);
    console.log(data.expected_cart);
    this.expected_cart = ko.observable(data.expected_cart) || "removals only";
}
    cartlogic.Ticket = Ticket;

})(window.cartlogic);
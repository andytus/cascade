/**
 *
 * User: jbennett
 * Date: 5/7/13
 * Time: 11:29 PM
 *
 */


//    id: 5,
//    service: "Audit",
//    code: "AUDIT",
//    description: "This is used for audit",
//    complete_cart_status_change: 6


(function (cartlogic){

    function TicketServices(data) {
        this.id = ko.observable(data.id);
        this.service = ko.observable(data.service);
        this.code = ko.observable(data.code);
        this.description = ko.observable(data.description)
        this.completed_cart_status_change = ko.observable(data.completed_cart_status_change)

    }

    cartlogic.TicketServices = TicketServices;


})(window.cartlogic);
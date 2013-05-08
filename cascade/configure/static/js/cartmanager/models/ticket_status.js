/**
 *
 * User: jbennett
 * Date: 5/2/13
 * Time: 4:06 PM
 *
 */



(function (cartlogic){

    function TicketStatusOption(data) {
        this.id = ko.observable(data.id);
        this.level = ko.observable(data.level);
        this.service_status = ko.observable(data.service_status);
    }
    cartlogic.TicketStatusOption = TicketStatusOption;

})(window.cartlogic);
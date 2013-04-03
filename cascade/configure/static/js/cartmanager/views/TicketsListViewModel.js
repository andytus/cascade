/**
 *
 * User: jbennett
 * Date: 2/28/13
 * Time: 9:17 AM
 *
 */


(function (cartlogic) {


    function TicketsViewModel() {
        var self = this;
        //setup some global variables for getting tickets:
        self.count = ko.observable(0);
        self.page = ko.observable(1);
        //#TODO Implement records per page (hard coded in html for now)
        self.records_per_page = ko.observable(100);
        self.total_pages = ko.computed(function () {
            return (Math.round(self.count() / self.records_per_page()));

        });
        self.sort_default = ko.observable('status__service_status');
        //cart tickets
        self.tickets = ko.observableArray();
        self.ticket_table_headers = ko.observableArray(
            //# Ugly but works
            [
                {field:'status__service_status', displayName:'Status', sort:ko.observable(0)},
                {field:'service_type__code', displayName:'Type', sort:ko.observable(0)},
                {field:'success_attempts', displayName:'Attempts', sort:ko.observable(0)},
                {field:'date_created', displayName:'Created', sort:ko.observable(0)},
                {field:'date_last_attempted', displayName:'Last Attempt', sort:ko.observable(0)},
                {field:'location__house_number', displayName:'House', sort:ko.observable(0)},
                {field:'location__street_name', displayName:'Street', sort:ko.observable(0)},
                {field:'location__unit', displayName:'Unit', sort:ko.observable(0)},
                {field:'serviced_cart__rfid', displayName:'Serviced RFID', sort:ko.observable(0)},
                {field:'expected_cart__rfid', displayName:'Expected RFID', sort:ko.observable(0)},
             ]
        );

        self.getTickets = function (page) {
            url = tickets_api_download;
            self.page(page); //update page

            //TODO Refactor to accept more data for searching tickets (i.e. Open, Type, ect...)
            data = {"page":self.page(), "sort_by":self.sort_default()};

            //check if serial and/or customer id is not undefined and add to the data load
            if (typeof cart_serial_number != 'undefined'&& cart_serial_number != null){
                data.serial_number = cart_serial_number;
            }

            if (typeof customer_id != 'undefined' && customer_id != null){
                data.customer_id = customer_id;
            }

            $.getJSON(url, data, function (data) {
               // console.log(customer_id);
                self.count(data.count);
                var cartTickets = $.map(data.results, function (item) {
                    return new cartlogic.Ticket(item);
                });
                self.tickets(cartTickets);
            });

        };

        self.sortTickets = function (page, sort_by) {

            for (var i = 0; i < self.ticket_table_headers().length; i++) {
                if (self.ticket_table_headers()[i].field != sort_by.field)
                    self.ticket_table_headers()[i].sort(0);
            }

            if (sort_by.sort() == 0) {
                sort_by.sort(1);
                self.sort_default(sort_by.field);
                self.getTickets(1);
             }

            else if (sort_by.sort() == 1) {
                sort_by.sort(2);
                //rest the current default to 0 sort
                console.log(sort_by.sort());
                self.sort_default("-" + sort_by.field);
                self.getTickets(1);
            }
            else {
                //rest the current default to 0 sort
                sort_by.sort(0);
            }

        };

        //#TODO call this on each page... refactor to accept more than just serial: SEE, http://stackoverflow.com/questions/6486307/default-argument-values-in-javascript-functions
        self.getTickets(1);

        //Setting the tickets to refresh on modal close, #TODO put in custom binding
        $('#modal_window').on('hidden', function () {
            //checking for not null serial number because we don't want a refresh of the ticket
           self.getTickets(1);


        });

    }

    cartlogic.TicketsViewModel = TicketsViewModel;

})(window.cartlogic);
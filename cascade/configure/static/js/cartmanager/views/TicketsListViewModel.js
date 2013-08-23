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
        self.ticket_table_headers = ko.observableArray(
            //# Ugly but works
            [
                {field:'status__service_status', displayName:'Status', sort:ko.observable(0)},
                {field:'service_type__code', displayName:'Type', sort:ko.observable(0)},
                {field:'cart_type__size', displayName:'Size', sort:ko.observable(0)},
                {field:'cart_type__name', displayName:'Cart Type', sort:ko.observable(0)},
                {field:'success_attempts', displayName:'Attempts', sort:ko.observable(0)},
                {field:'date_created', displayName:'Created', sort:ko.observable(0)},
                {field:'date_last_attempted', displayName:'Last Attempt', sort:ko.observable(0)},
                {field:'location__house_number', displayName:'House', sort:ko.observable(0)},
                {field:'location__street_name', displayName:'Street', sort:ko.observable(0)},
                {field:'location__unit', displayName:'Unit', sort:ko.observable(0)},
                {field:'serviced_cart__serial_number', displayName:'Serviced #', sort:ko.observable(0)},
                {field:'expected_cart__serial_number', displayName:'Expected #', sort:ko.observable(0)}
            ]
        );

        //cart tickets
        self.tickets = ko.observableArray();

        self.getTickets = function (page, sort_by, format, status, service, cart_type, size) {
            self.page(page); //update page
            //sort logic only used when clicking on header
            if (typeof sort_by != 'undefined' && sort_by != null) {
                for (var i = 0; i < self.ticket_table_headers().length; i++) {
                    if (self.ticket_table_headers()[i].field != sort_by.field)
                        self.ticket_table_headers()[i].sort(0);
                }

                if (sort_by.sort() == 0) {
                    sort_by.sort(1);
                    self.sort_default(sort_by.field);

                }

                else if (sort_by.sort() == 1) {
                    sort_by.sort(2);
                    //reset the current default to 0 sort
                    self.sort_default("-" + sort_by.field);

                }
                else {
                    //reset the current default to 0 sort
                    sort_by.sort(0);
                }

            }

            //TODO Refactor to accept more data for searching tickets (i.e. Open, Type, ect...)
            //TODO ugly way to test for search options, which are global

            var search_by = {};

            //Check if status is not undefined
            if (typeof status != 'undefined') {
                search_by.status = status;
            }

            if (typeof service != 'undefined') {
                search_by.service = service
            }

            if (typeof cart_type != 'undefined') {
                search_by.cart_type = cart_type
            }

            if (typeof size != 'undefined') {
                search_by.cart_size = size;
            }


            //check if serial and/or customer id is not undefined and add to the data load
            if (typeof cart_serial_number != 'undefined' && cart_serial_number != null) {
                search_by.serial_number = cart_serial_number;
            }

            if (typeof customer_id != 'undefined' && customer_id != null) {
                search_by.customer_id = customer_id;
            }

            //making sure the search_by is not empty
            if (!jQuery.isEmptyObject(search_by)) {

                var data = {page:self.page(), sort_by:self.sort_default(), format: format};
                //adding search_by to data
                data.search_by = ko.toJSON(search_by);

                if(format == 'csv'){
                    //if it is a csv format just load in the window (no ajax needed).
                    window.location = tickets_api_download  + "?" + jQuery.param(data);
                } else{

                $.ajax(tickets_api_download, {
                    data:data,
                    dataType: format,
                    type:"get", contentType:"application/json",
                    success:function(data){
                        self.count(data.count);
                        var cartTickets = $.map(data.results, function (item) {
                            return new cartlogic.Ticket(item);
                        });
                        self.tickets(cartTickets);

                    },
                    error:function (jqXHR) {
                        $("#message").addClass("alert-error").show();
                        $("#message-type").text("Error!");
                        $("#message-text").text(jqXHR.statusText);
                        $('.close').click(function () {
                        $('#message').hide();
                        });


                    }
                });
                }
            }
        };

        /*    self.sortTickets = function (page, sort_by) {

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
         //reset the current default to 0 sort
         self.sort_default("-" + sort_by.field);
         self.getTickets(1);
         }
         else {
         //reset the current default to 0 sort
         sort_by.sort(0);
         }

         };*/

        //#TODO call this on each page... refactor to accept more than just serial: SEE, http://stackoverflow.com/questions/6486307/default-argument-values-in-javascript-functions
        self.getTickets(1, null, 'json');

        //Setting the tickets to refresh on modal close
        $('#modal_window').on('hidden', function () {
            //#TODO Fix returning all tickets after removal
            //checking for not null serial number because we don't want a refresh of the ticket if (typeof yourvar != 'undefined')

            self.getTickets(1, null, 'json')

        });


    }

    cartlogic.TicketsViewModel = TicketsViewModel;

})(window.cartlogic);
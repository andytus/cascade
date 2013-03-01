/**
 *
 * User: jbennett
 * Date: 2/28/13
 * Time: 9:17 AM
 *
 */


(function (cartlogic){


function TicketsViewModel() {
    var self = this;
    self.count = ko.observable(0);
    self.page = ko.observable(1);
    //#TODO Implement records per page (hard coded in html for now)
    self.records_per_page = ko.observable(40);
    self.total_pages = ko.computed(function () {
        return (Math.round(self.count() / self.records_per_page()));

    });
    self.sort_default = ko.observable('status__service_status');
    //cart tickets
    self.tickets = ko.observableArray();
    self.ticket_table_headers = ko.observableArray(
        //#TODO ugly but works
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
            {field:'expected_cart__rfid', displayName:'Expected RFID', sort:ko.observable(0)}
        ]
    );

    self.getTickets = function (serial_number, page) {
        url = tickets_api_download;
        self.page(page); //update page

        //TODO Refactor to accept more data for searching tickets (i.e. Open, Type, ect...)
        data = {"serial_number":serial_number, "page":page, "sort_by":self.sort_default()};


        $.getJSON(url, data, function (data) {
            self.count(data.count);
            var cartTickets = $.map(data.results, function (item) {
                return new cartlogic.Ticket(item);
            });
            self.tickets(cartTickets);
        });
    };

    self.sortTickets = function (serial_number, page, sort_by) {

        for (var i=0; i < self.ticket_table_headers().length; i++){
            if (self.ticket_table_headers()[i].field != sort_by.field)
                self.ticket_table_headers()[i].sort(0);
        }

        if (sort_by.sort() == 0) {
            sort_by.sort(1);
            self.sort_default(sort_by.field);
            self.getTickets(serial_number, 1);

        }

        else if (sort_by.sort() == 1) {
            sort_by.sort(2);
            //rest the current default to 0 sort
            console.log(sort_by.sort());
            self.sort_default("-" + sort_by.field);
            self.getTickets(serial_number, 1);
        }
        else {
            //rest the current default to 0 sort
            sort_by.sort(0);
        }

    };

    self.createNewTicket = function(serial_number){
        //Note: if serial_number = new, then this function will create a new ticket
        //#TODO working on creating a ticket
        console.log(cart_profile.size);

        $.ajax(ticket_api + serial_number, {
                data:ko.toJSON({'test':"foo me"}),
                type:"post", contentType:"application/json",
                dataType:"jsonp"
            }

        )

    };

    //#TODO call this on each page... refactor to accept more than just serial:
    self.getTickets(serial_number, 1);
}

cartlogic.TicketsViewModel = TicketsViewModel;

})(window.cartlogic);
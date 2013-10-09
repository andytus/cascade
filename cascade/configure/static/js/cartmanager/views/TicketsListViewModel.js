/**
 *
 * User: jbennett
 * Date: 2/28/13
 * Time: 9:17 AM
 *
 */


(function (cartlogic) {

    function TicketsListViewModel(cart_serial_number, customer_id, tickets_api_download) {

        var self = this;
        self.tickets = ko.observableArray([]);
        self.sortOnServer = ko.observable(false);
        self.sortInfo = ko.observable();

        self.status = ko.observable("Requested");
        self.service = ko.observable("ALL");
        self.cart_type = ko.observable("ALL");
        self.cart_size = ko.observable("ALL");
        self.route_type = ko.observable("ALL");
        self.route_day = ko.observable("ALL");
        self.route = ko.observable('ALL');
        self.sort_by = ko.observable('id');

        self.cart_serial_number = ko.observable(cart_serial_number);
        self.customer_id = ko.observable(customer_id);
        self.pagingOptions = {
            pageSizes: ko.observableArray([100, 250, 500]),
            pageSize: ko.observable(100),
            totalServerItems: ko.observable(0),
            currentPage: ko.observable(1)
        };

        this.getPagedDataAsync = function () {
            var data = {};
            data.page = self.pagingOptions.currentPage();
            data.page_size = self.pagingOptions.pageSize();
            data.sort_by = self.sort_by();

            if (typeof self.cart_serial_number() != 'undefined' && self.cart_serial_number() != null) {
                data.serial_number = self.cart_serial_number();
            }

            else if (typeof self.customer_id() != 'undefined' && self.customer_id() != null) {
                data.customer_id = self.customer_id();
            }
            else {
                data.cart_size = self.cart_size();
                data.cart_type = self.cart_type();
                data.service = self.service();
                data.status = self.status();
                data.route = self.route();
                data.route_type = self.route_type();
                data.route_day = self.route_day();
            }

            $.ajax(tickets_api_download, {
                data: data,
                dataType: 'jsonp',
                type: "get", contentType: "application/json",
                success: function (data) {
                    var cartTickets = $.map(data.results, function (item) {
                        return new cartlogic.Ticket(item);
                    });
                    self.tickets(cartTickets);
                    self.pagingOptions.totalServerItems(data.count)
                },
                error: function (jqXHR) {
                    $("#message").addClass("alert-error").show();
                    $("#message-type").text("Error!");
                    $("#message-text").text(" " + jqXHR.statusText);
                    $(".close").click(function () {
                        $("#message").hide();

                    });

                }
            });

        };

        //Listens for a click on a run ticket query and downloads a csv or calls ajax function
        $('.run_query').click(function () {

            var context = (ko.contextFor(this));
            console.log(context.$data.selected_route().route(), context.$data.selected_route_day());
            self.cart_size(context.$data.selected_cart_size());
            self.cart_type(context.$data.selected_cart_type());
            self.service(context.$data.selected_type());
            self.status(context.$data.selected_status());
            self.route_type(context.$data.selected_route_type());
            self.route_day(context.$data.selected_route_day());
            self.route(context.$data.selected_route().route());

            if (this.id == 'download_csv') {
                //if it is a csv format just load in the window (no ajax needed).
                var data = {};
                data.cart_size = self.cart_size();
                data.cart_type = self.cart_type();
                data.service = self.service();
                data.status = self.status();
                data.route_type = self.route_type();
                data.route_day = self.route_day();
                data.route = self.route();
                window.location = tickets_api_download + "?format=csv&" + jQuery.param(data);
            } else {
                self.getPagedDataAsync();
            }

        });

        self.pagingOptions.currentPage.subscribe(function (page) {
            //setter for current page
            self.pagingOptions.currentPage(page);
            self.getPagedDataAsync();
        });

        self.pagingOptions.pageSize.subscribe(function (pageSize) {
            //setter for pageSize
            self.pagingOptions.pageSize(pageSize);
            self.getPagedDataAsync();

        });

        self.sortInfo.subscribe(function (data) {

            //work around because koGrid bug calls sort twice:
            // See: http://stackoverflow.com/questions/15232644/kogrid-sorting-server-side-paging
            self.sortOnServer(!self.sortOnServer());
            if (!self.sortOnServer()) return;

            self.sort_by(self.sortInfo().column.field);
            if (self.sortInfo().direction == 'desc') {
                self.sort_by("-" + self.sort_by())
            }
           self.getPagedDataAsync();

        });

        self.cart_profile_cell_template = '<a data-bind=" attr:{ \'href\' : \'' + cart_app_profile_url +
            '\' + $data.getProperty($parent)}, text:  $data.getProperty($parent)"></a>';

        self.ticket_profile_cell_open_template = '<a style=\'margin-top: 1px;\' class=\' btn btn-small, btn-info\'data-bind="attr: {\'href\' : \''
            + ticket_app_profile_url + '\' + $data.getProperty($parent)}, text: ' +
            '\'Open: \' +  $data.getProperty($parent)">Open</a>';

        self.columns = [
            {field: 'id', displayName: "Open", cellTemplate: self.ticket_profile_cell_open_template, width: 110},
            {field: 'status__service_status', displayName: 'Status'},
            {field: 'service_type__code', displayName: 'Type'},
            {field: 'cart_type__name', displayName: 'Cart Type'},
            {field: 'cart_type__size', displayName: 'Size'},
            {field: 'success_attempts', displayName: 'Tries', width: 50},
            {field: 'location__house_number', displayName: 'House'},
            {field: 'location__street_name', displayName: 'Street', width: 165, maxWidth: 400},
            {field: 'location__unit', displayName: 'Unit', width: 50},
            {field: 'serviced_cart__serial_number', displayName: 'Serviced #', cellTemplate: self.cart_profile_cell_template, width: 100},
            {field: 'expected_cart__serial_number', displayName: 'Expected #', cellTemplate: self.cart_profile_cell_template, width: 100},
            {field: 'date_created', displayName: 'Created'},
            {field: 'date_last_attempted', displayName: 'Last Try'}

        ];

        self.gridOptions = {
            data: self.tickets,
            enablePaging: true,
            useExternalSorting: true,
            pagingOptions: self.pagingOptions,
            sortInfo: self.sortInfo,
            columnDefs: self.columns,
            canSelectRows: false,
            footerRowHeight: 50,
            selectWithCheckboxOnly: true,
            showFilter: false

        }


    $('#modal_window').on('hidden', function(){
        //need to refresh the ticket panel on add of new ticket form a modal window
        self.getPagedDataAsync();
    })


    }
;

    cartlogic.TicketsListViewModel = TicketsListViewModel;

})(window.cartlogic);
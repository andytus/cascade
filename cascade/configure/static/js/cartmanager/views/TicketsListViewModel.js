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

        self.status = ko.observableArray(["Requested"]);
        self.service = ko.observable("ALL");
        self.cart_type = ko.observable("ALL");
        self.cart_size = ko.observable("ALL");
        self.route_type = ko.observable("ALL");
        self.route_day = ko.observable("ALL");
        self.route = ko.observable('ALL');
        self.sort_by = ko.observable('id');
        self.search_to_date = ko.observable(null);
        self.search_from_date = ko.observable(null);
        self.search_days = ko.observable('ALL');
        self.search_days_type = ko.observable('Created');
        self.charge = ko.observable('ALL');
        self.no_charges = ko.observable(false);
        self.report_type = ko.observable('service_ticket');


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
            //will grab all the ticket for a specific cart
            if (typeof self.cart_serial_number() != 'undefined' && self.cart_serial_number() != null) {
                data.serial_number = self.cart_serial_number();
            }
            //will grab all the tickets for a specific customer
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
                data.search_days = self.search_days();
                data.search_days_type = self.search_days_type();
                data.charge = self.charge();
                data.no_charges = self.no_charges();

                if (self.search_from_date() != 'undefined' && self.search_from_date() != null) {
                    data.search_to_date = self.search_to_date();
                    data.search_from_date = self.search_from_date()
                }


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
            //set ticket list params
            var context = (ko.contextFor(this));
            self.cart_size(context.$data.selected_cart_size());
            self.cart_type(context.$data.selected_cart_type());
            self.service(context.$data.selected_type());
            self.status(context.$data.selected_status());
            self.route_type(context.$data.selected_route_type());
            self.route_day(context.$data.selected_route_day());
            self.route(context.$data.selected_route().route());
            self.search_days(context.$data.selected_search_days().value);
            self.charge(context.$data.selected_charge());
            self.no_charges(context.$data.no_charges());
            self.search_days_type(context.$data.search_days_type());
            self.search_to_date(context.$data.search_to_date());
            self.search_from_date(context.$data.search_from_date());


            //TODO refactor for redundancy....
            if (this.id == 'download_csv') {
                //if it is a csv format just load in the window (no ajax needed).
                var data = {};
                data.status = [];
                data.cart_size = self.cart_size();
                data.cart_type = self.cart_type();
                data.service = self.service();
                data.status.push(self.status());
                data.route_type = self.route_type();
                data.route_day = self.route_day();
                data.route = self.route();
                data.search_days = self.search_days();
                data.search_days_type = self.search_days_type();
                if (self.search_from_date() != 'undefined' && self.search_from_date() != null) {
                    data.search_to_date = self.search_to_date();
                    data.search_from_date = self.search_from_date();
                }
                data.charge = self.charge();
                data.no_charges = self.no_charges();
                //just getting report type directing from TicketsListViewModel
                //don't need for displayed report
                data.report_type = self.report_type().report;
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

        self.cart_profile_cell_template = '<p data-bind="attr: { \'class\': \'kgCellText colt \' + $index()}">' +
            '<a data-bind=" attr:{ \'href\' : \'' + cart_app_profile_url +
            '\' + $data.getProperty($parent)}, text:  $data.getProperty($parent)"></a></p>';

        self.ticket_profile_cell_open_template = '<a style=\'margin-top: 1px;\' class=\' btn btn-small, btn-info \'data-bind="attr: {\'href\' : \''
            + ticket_app_profile_url + '\' + $data.getProperty($parent)}, text: $data.getProperty($parent)">Open</a>';

        self.money_format = '<p  data-bind= "text: \'$\' + $parent.entity[\'charge\'](), attr: { \'class\': \'kgCellText colt \' + $index()}"></p>';


        self.time_format = '<span data-bind= "text: new cartlogic.TimeFormat($parent.entity[\'date_last_attempted\'])></span>'

        self.columns = [
            {field: 'id', displayName: "Open", cellTemplate: self.ticket_profile_cell_open_template, width: 100},
            {field: 'status__service_status', displayName: 'Status', width: "***"},
            {field: 'service_type__code', displayName: 'Type', width: "**"},
            {field: 'charge', displayName: 'Charge', cellTemplate: self.money_format, width: "**"},//'<span data-bind="text:"$data.getProperty($parent)> </span>'},
            {field: 'cart_type__name', displayName: 'Cart Type', width: "**"},
            {field: 'cart_type__size', displayName: 'Size', width: "**"},
            {field: 'success_attempts', displayName: 'Tries', width: "*"},
            {field: 'location__house_number', displayName: 'House', width: "**"},
            {field: 'location__street_name', displayName: 'Street', width: "***"},
            {field: 'location__unit', displayName: 'Unit', width: "**"},
            {field: 'route__route', displayName: 'Route', width: "**"},
            {field: 'serviced_cart__serial_number', displayName: 'Serviced #', cellTemplate: self.cart_profile_cell_template, width: "******"},
            {field: 'expected_cart__serial_number', displayName: 'Expected #', cellTemplate: self.cart_profile_cell_template, width: "******"},
            {field: 'date_last_attempted', displayName: 'Last Try', width: 120},
            {field: 'date_created', displayName: 'Created', width: "****"}


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


        $('#modal_window').on('hidden', function () {
            //need to refresh the ticket panel on add of new ticket form a modal window
            self.getPagedDataAsync();
        })


    }
    ;

    cartlogic.TicketsListViewModel = TicketsListViewModel;

})(window.cartlogic);
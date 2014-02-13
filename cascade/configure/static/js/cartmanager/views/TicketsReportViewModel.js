/**
 *
 * User: jbennett
 * Date: 5/7/13
 * Time: 10:04 PM
 *
 */


(function (cartlogic) {

    function TicketsReportViewModel(data) {
        var self = this;

        self.selected_type = ko.observable();
        self.selected_status = ko.observableArray(['Requested']);
        self.selected_cart_type = ko.observable();
        self.selected_cart_size = ko.observable();
        self.selected_route = ko.observable();
        self.selected_route_type = ko.observable();
        self.selected_route_day = ko.observable();
        self.selected_search_days = ko.observable();
        self.selected_charge = ko.observable();
        self.no_charges = ko.observable(false);

        //options for select drop downs
        self.ticket_type_options = ko.observableArray([]);
        self.ticket_status_options = ko.observableArray([]);
        self.cart_type_options = ko.observableArray([]);
        self.cart_size_options = ko.observableArray([]);
        self.service_charge_options = ko.observableArray([]);
        self.routes = ko.observableArray([]);
        self.route_days = ko.observableArray([]);
        self.route_types = ko.observableArray([]);
        self.search_to_date = ko.observable();
        self.search_from_date = ko.observable();
        self.search_days_type = ko.observable('Created');
        self.search_days_type_options = ko.observableArray(['Created', 'Completed']);
        self.search_days = ko.observableArray(
            [
                {'display': 'Day', 'value': 1},
                {'display': 'Three days', 'value': 3},
                {'display': 'Week', 'value': 7},
                {'display': 'Two weeks', 'value': 14},
                {'display': 'Month', 'value': 30},
                {'display': 'Year', 'value': 365},
                {'display': 'Millennium', 'value': 'ALL'}
            ]
        )

        self.ticket_report_options = ko.observableArray([
            {'display': "Handheld Tickets", 'report': 'service_tickets'},
            {'display': 'Service Charges', 'report': 'service_charges'}
        ]);


        self.filtered_routes = ko.computed(function () {
            var filtered_routes = ko.utils.arrayFilter(self.routes(), function (item) {
                    //check if cart type (i.e. same as route) is ALL
                    if (self.selected_route_type() == 'ALL') {
                        //then check if route day is also ALL and return all routes
                        if (self.selected_route_day() == 'ALL') {
                            return item;
                            //if its not all then filter by day
                        } else if (self.selected_route_day() == item.route_day()) {
                            return item;
                        }
                        // else check if route day is ALL
                    } else if (self.selected_route_day() == 'ALL') {
                        // if the selected cart type is the same as the route type return the route
                        if (self.selected_route_type() == item.route_type()) {
                            return item;
                        }
                        //else filter by both route day and cart type
                    } else if (self.selected_route_day() == item.route_day()
                        && self.selected_route_type() == item.route_type()) {
                        return item;
                    }
                }
            );

            self.selected_route_type.subscribe(function (data) {
                self.selected_cart_type(data);
            });

            var all_route = new cartlogic.Route({'id': 'ALL', 'route_day': 'ALL',
                'route_type': 'ALL', 'route': 'ALL'});
            filtered_routes.unshift(all_route);
            return filtered_routes;
        });

        self.search_days_type.subscribe(function (data) {
            if (data == 'Completed') {
                self.selected_status('Completed');
            } else {
                self.selected_status('ALL');
            }

        });


        self.date_change = function () {
            var day_match = ko.utils.arrayFirst(self.search_days(), function (item) {
                return item.display == 'Millennium'
            });
            ;
            self.selected_search_days(day_match);
            self.selected_search_days().value = 'ALL';

            var from = new Date(self.search_from_date());
            var to = new Date(self.search_to_date());

            if (from > to) {
                $("#message").addClass("alert-warning").show();
                $("#message-text").text("Hey Silly...From  date must 'before' To date");
                $(".close").click(function () {
                    $("#message").hide();
                });
            }

        }

        self.search_from_date.subscribe(function (data) {
            self.date_change();
        })

        self.search_to_date.subscribe(function (data) {
            self.date_change()
        })


        self.getServiceTypeOptions = function () {
            $.getJSON(ticket_service_type_api, function (data) {
                var serviceTypeOptions = $.map(data, function (item) {
                    return item.service
                });
                self.ticket_type_options(serviceTypeOptions);
                self.ticket_type_options.unshift('ALL');
                var type_match = ko.utils.arrayFirst(self.ticket_type_options(), function (item) {
                    return item == 'ALL'
                });
                self.selected_type(type_match);
            });
        };


        self.getServiceCharges = function () {
            $.getJSON(cart_service_charge_api_url, function (data) {
                var serviceChargesOptions = $.map(data, function (item) {
                    return item.amount
                });
                self.service_charge_options(serviceChargesOptions);
                self.service_charge_options.unshift('ALL');
                var type_match = ko.utils.arrayFirst(self.service_charge_options(), function (item) {
                    return item == 'ALL'
                });
                self.selected_charge(type_match);
            })
        }

        self.getServiceStatusOptions = function () {
            $.getJSON(ticket_status_api, function (data) {
                var ticketStatusOptions = $.map(data, function (item) {
                    return item.service_status;
                });
                self.ticket_status_options(ticketStatusOptions);
                var match = ko.utils.arrayFirst(self.ticket_status_options(), function (item) {
                    return item === 'Requested';
                });
                self.selected_status(match);

                 $('.multiselect').multiselect({ includeSelectAllOption: true }).multiselect('select', 'Requested');

            });
        };

        self.getRouteOptions = function () {
            $.getJSON(route_search_api_url + "?format=jsonp&callback=?", function (data) {
                    var routeDayOptions = [];
                    var routeTypeOptions = [];


                    //get unique types and days
                    $.each(data.results, function (index, item) {
                        if ($.inArray(item.route_day, routeDayOptions) == -1) {
                            routeDayOptions.push(item.route_day);
                        }
                        if ($.inArray(item.route_type, routeTypeOptions) == -1) {
                            routeTypeOptions.push(item.route_type);
                        }
                    });

                    var routeOptions = $.map(data.results, function (item) {
                        return new cartlogic.Route(item);
                    });
                    self.route_days(routeDayOptions);
                    self.route_types(routeTypeOptions);
                    self.routes(routeOptions);

                    self.route_days.unshift('ALL');
                    self.route_types.unshift('ALL');
                    self.selected_route_day('ALL');
                    self.selected_route_type('ALL');
                }
            );
        };


        self.getCartTypeOptions = function () {
            url = cart_type_api + "?format=jsonp&callback=?";
            $.getJSON(url, data, function (data) {
                var cartTypeOptions = [];
                var cartSizeOptions = [];

                //build CartTypeOption & cartSizeOptions array
                //get only unique cart sizes and type
                $.each(data, function (index, item) {
                    if ($.inArray(item.name, cartTypeOptions) == -1) {
                        cartTypeOptions.push(item.name);
                    }
                    if ($.inArray(item.size, cartSizeOptions) == -1) {
                        cartSizeOptions.push(item.size);
                    }
                });

                self.cart_type_options(cartTypeOptions);
                self.cart_size_options(cartSizeOptions);
                self.cart_type_options.unshift('ALL');
                self.cart_size_options.unshift('ALL');

                var size_match = ko.utils.arrayFirst(self.cart_size_options(), function (item) {
                    return item == 'ALL'
                });

                self.selected_cart_size(size_match);

                var day_match = ko.utils.arrayFirst(self.search_days(), function (item) {
                    return  item.value == 'ALL'
                });
                self.selected_search_days(day_match);

                var type_match = ko.utils.arrayFirst(self.cart_type_options(), function (item) {
                    return item == 'ALL'
                });
                self.selected_cart_type(type_match);
            });
        };

        self.addCalendar = function () {
            //putting in a date and time picker
            $('.datepicker').datepicker({
                format: 'mm-dd-yyyy'
            });
        }

        $('#reset_params').click(function () {

            //Reset all query parameters TODO: refactor to call this at page load

            //Reset Ticket status
            self.selected_status = ko.observable('Requested');
            //Reset Ticket type
            var ticket_type_match = ko.utils.arrayFirst(self.ticket_type_options(), function (item) {
                return item == 'ALL'
            });
            self.selected_type(ticket_type_match);
            //Reset Cart type
            var cart_type_match = ko.utils.arrayFirst(self.cart_type_options(), function (item) {
                return item == 'ALL'
            });
            self.selected_cart_type(cart_type_match);
            //Reset Cart size
            var size_match = ko.utils.arrayFirst(self.cart_size_options(), function (item) {
                return item == 'ALL'
            });
            self.selected_cart_size(size_match);
            //Reset report
            //TODO implement

            //Reset Days
            var day_match = ko.utils.arrayFirst(self.search_days(), function (item) {
                return  item.value == 'ALL'
            });
            self.selected_search_days(day_match);

            //Reset search to and from dates
            self.search_to_date("");
            self.search_from_date("");

            //Reset Route day and Type
            self.selected_route_day('ALL');
            self.selected_route_type('ALL');

            //Reset Routes
            var route_match = ko.utils.arrayFirst(self.filtered_routes(), function(item){
                return item.route() == 'ALL'
            })
            self.selected_route(route_match);


            //Reset charges
            var type_match = ko.utils.arrayFirst(self.service_charge_options(), function (item) {
                return item == 'ALL'
            });
            self.selected_charge(type_match);

            //Reset no charges
            self.no_charges(false)


        });


        self.addCalendar();
        self.getServiceTypeOptions();
        self.getServiceStatusOptions();
        self.getCartTypeOptions();
        self.getRouteOptions();
        self.getServiceCharges();

    }

    cartlogic.TicketsReportViewModel = TicketsReportViewModel;

})(window.cartlogic);
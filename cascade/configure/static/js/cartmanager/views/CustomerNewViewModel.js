(function (cartlogic) {

    function CustomerNewViewModel() {

        var self = this;

        self.server_message = ko.observable();
        self.server_message_type = ko.observable();

        //creates a blank customer
        self.customer = ko.observable(new cartlogic.Customer);
        self.location = ko.observable(new cartlogic.Location);
        //location information

        self.suffix = ko.observable();


        //state and city, can use a default
        self.use_default_state_city = ko.observable(true);

        self.default_zipcodes = ko.observableArray([]);


        self.default_property_type = ko.observableArray(['Residential', 'Business']);
        self.selected_route_day = ko.observable();
        self.selected_route_type = ko.observable();
        self.selected_route = ko.observable();

        //these get sent to the server
        self.selected_routes = ko.observableArray([]);

        self.default_routes = ko.observableArray([]);
        self.default_routes_unique_type = ko.computed(function () {
            var route_type = ko.utils.arrayMap(self.default_routes(), function(item) {
                return item.route_type();
            });
            route_type.unshift('ALL')
            return ko.utils.arrayGetDistinctValues(route_type);
        });

        self.default_routes_unique_day = ko.computed(function () {
            var route_days = ko.utils.arrayMap(self.default_routes(), function(item) {
                return item.route_day();
            });

            route_days.unshift('ALL')
            return ko.utils.arrayGetDistinctValues(route_days.sort());
        });

        self.default_routes_unique_routes = ko.computed(function () {
            var filtered_routes = ko.utils.arrayFilter(self.default_routes(), function(item) {
                if (self.selected_route_day() == item.route_day()
                    && self.selected_route_type() == item.route_type()) {
                    return item;
                }
            });
            var routes = ko.utils.arrayMap(filtered_routes, function (item) {
                return item;
            })
               return routes;
        });


        self.addRoute = function(){
            self.selected_routes.push({route:self.selected_route().route(),
                                       route_day:self.selected_route().route_day(),
                                       route_type:self.selected_route().route_type()
                                      });
            self.selected_route_day('ALL');
            self.selected_route_type("ALL");
        }

        self.clearRoute = function(){

            self.selected_routes.removeAll();

        }

        self.map_style = new cartlogic.MapStyle();

        self.geocoder_type = ko.observable('google');

        self.updateLocation = function () {
            //have to scrap geocode data from the DOM
            self.location().latitude($('#address_lat').val());
            self.location().longitude($('#address_lon').val());
            self.location().geocode_status($('#geocode_status').val());
        };

        self.mapIt = function () {
            var map_verify = new cartlogic.FormStep(3, "Map Verify", "MapLocation", {message: "Verify Location"});
            //Only add this step if its not been added
            if (self.stepModels().length <= 5) {
                self.stepModels.splice(2, 0, map_verify);
            }
            self.currentStep(self.stepModels()[2]);
            //just give the map a little time to load:
            var address_map = new cartlogic.GeocodeMap(document.getElementById('map_canvas_address'), 'address_lat',
                'address_lon', 'geocode_status', {coder: self.geocoder_type(),
                    address: self.location().full_address_ci_st_zip()});
            //do the mapping:
            address_map.geocode();
        };

        self.stepModels = ko.observableArray([
            new cartlogic.FormStep(1, "Add Customer Information", "CustomerInfo",
                {message: "Create New Customer Wizard" }),
            new cartlogic.FormStep(2, "Add Address Information", "AddressInfo", {message: "Add Address"}),
            new cartlogic.FormStep(4, "Add Route", "AddRoute", {message: "Add Route"}),
            new cartlogic.FormStep(5, "Confirm Save", "ConfirmSave", {message: "Confirm Save"}),
            new cartlogic.FormStep(6, "Complete", "Complete", {message: "Verify Location"})
        ]);

        self.get_default_info = function () {
            url = admin_api_location + "?format=jsonp&callback=?";

            $.getJSON(url, function (data) {
                self.location().state(data.info.state);
                self.location().city(data.info.city);
                var zipcodes = $.map(data.info.zipcodes, function (item) {
                    return item.zipcode;
                });
                self.default_zipcodes(zipcodes);
                //adding blank at the beginning
               //$("#cart-info-edit-status option[value='" + self.cart().current_status_id() + "']").attr("selected", "selected");
            });
        };

        self.saveAddress = function () {
            data = {customer_id: self.customer().customer_id(), house_number: self.location().house_number(),
                street_name: self.location().street_name(), suffix: self.location().suffix(),
                direction: self.location().direction(), city: self.location().city(), state: self.location().state(),
                zipcode: self.location().zipcode(), property_type: self.location().property_type(),
                geocode_status: self.location().geocode_status()};

            if (self.location().unit()) {
                data.unit = self.location().unit()
            }

            if (self.location().latitude()) {
                data.latitude = self.location().latitude();
            }

            if (self.location().longitude()) {
                data.longitude = self.location().longitude();
            }

            if (self.selected_routes().length > 0){
                data.routes = ko.toJSON(self.selected_routes);
            }

            $.ajax(location_api_profile + 'New', {
                    data: ko.toJSON(data),
                    dataType: "jsonp",
                    type: "post", contentType: "application/json",
                    success: function (data) {
                        self.server_message_type(data.details.message_type);
                        self.server_message(self.server_message() + "<br>" + data.details.message);
                        //send message to last step
                        self.currentStep(self.stepModels()[self.stepModels().length - 1]);
                    },
                    error: function (jqXHR) {
                        //send error message to last step
                        self.currentStep(self.stepModels()[self.stepModels().length - 1]);
                        self.server_message_type("Failed");
                        self.server_message(jqXHR.statusText);

                    }

                }
            )

        };

        self.getRouteOptions = function () {

            $.getJSON(route_search_api_url + "?format=jsonp&callback=?", function (data) {
                    var RouteOptionsList = $.map(data.results, function (item) {
                        return new cartlogic.Route(item);
                    });
                    self.default_routes(RouteOptionsList);
               }

            );
        };

        self.saveCustomer = function () {
            if (self.customer().first_name() == " "){
                self.customer().first_name("RESIDENT")
            }
            if (self.customer().last_name() == " "){
                self.customer().last_name("RESIDENT")
            }

            data = ko.toJSON(self.customer);
            $.ajax(customer_api_url + 'New', {
                    data: data,
                    type: "post", contentType: "application/json",
                    dataType: "jsonp",
                    success: function (data) {
                        self.customer().customer_id(data.details.customer_id);
                        self.saveAddress();
                        self.server_message(data.details.message);
                    },
                    error: function (jqXHR, status, error) {
                        //send error message to last step
                        self.currentStep(self.stepModels()[self.stepModels().length - 1]);
                        self.server_message_type("failed");
                        self.server_message(jqXHR.statusText);

                    }

                }

            );


        };


        //Wizard Step Navigation

        self.currentStep = ko.observable(self.stepModels()[0]);

        self.currentIndex = ko.computed(function () {

            return self.stepModels.indexOf(self.currentStep());
        });

        self.isConfirmStep = ko.computed(function () {
            return self.currentIndex() == self.stepModels().length - 2;

        });


        self.isCompleteStep = ko.computed(function () {
            return self.currentIndex() == self.stepModels().length - 1;
        });

        self.canGoNext = ko.computed(function () {
            return self.currentIndex() < self.stepModels().length - 2;
        });


        self.goNext = function () {
            if (self.canGoNext()) {
                if (self.currentStep().id == 4) {
                    self.updateLocation();
                }
                self.currentStep(self.stepModels()[self.currentIndex() + 1]);
            }
        };

        self.canGoPrevious = ko.computed(function () {
            //can go to previous if the index is greater than zero and less than the last step (i.e. success)
            return self.currentIndex() > 0 && self.currentIndex() < self.stepModels().length - 1;
        });

        self.goPrevious = function () {
            if (self.canGoPrevious()) {
                self.currentStep(self.stepModels()[self.currentIndex() - 1]);
            }
        };

        self.get_default_info();
        self.getRouteOptions();

    }

    cartlogic.CustomerNewViewModel = CustomerNewViewModel


})(window.cartlogic);



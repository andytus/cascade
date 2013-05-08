(function (cartlogic) {

    function CustomerNewViewModel() {

        var self = this;

        self.server_message = ko.observable();
        self.server_message_type = ko.observable();

        //creates a blank customer
        self.customer = ko.observable(new cartlogic.Customer);
        self.location = ko.observable(new cartlogic.Location);
        //location information
        //TODO call server to get unique street after length of say 4
        self.update_street = function () {

        };

        // self.street_suffix = ko.observable();
        self.suffix_defaults = new cartlogic.streetSuffix().get_abbreviated();


        //state and city, can use a default
        self.use_default_state_city = ko.observable(true);

        self.default_zipcodes = ko.observableArray([]);
        //#TODO Pull from admin config
        self.default_property_type = ko.observableArray(['Residential', 'Business']);

        self.map_style = new cartlogic.MapStyle();


        self.geocoder_type = ko.observable('google');


        self.updateLocation = function(){
            //have to scrap geocode data from the DOM
            self.location().latitude($('#address_lat').val() );
            self.location().longitude($('#address_lon').val());
            self.location().geocode_status($('#geocode_status').val());
        };


        self.mapIt = function () {
            var map_verify = new cartlogic.FormStep(3, "Map Verify", "MapLocation", {message:"Verify Location"});
            //Only add this step if its not been added
            if (self.stepModels().length <= 4) {
                self.stepModels.splice(2, 0, map_verify);
            }
            self.currentStep(self.stepModels()[2]);
            //just give the map a little time to load:
            var address_map = new cartlogic.GeocodeMap(document.getElementById('map_canvas_address'), 'address_lat', 'address_lon', 'geocode_status', {coder:self.geocoder_type(), address:self.location().full_address_ci_st_zip()});
            //do the mapping:
            address_map.geocode();

        };


        self.stepModels = ko.observableArray([

            new cartlogic.FormStep(1, "Add Customer Information", "CustomerInfo",
                {message:"Create New Customer Wizard" }),

            new cartlogic.FormStep(2, "Add Address Information", "AddressInfo", {message:"Add Address"}),

            new cartlogic.FormStep(4, "Confirm Save", "ConfirmSave", {message:"Confirm Save"}),

            new cartlogic.FormStep(5, "Complete", "Complete", {message:"Verify Location"})

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
                self.default_zipcodes.unshift('Select One');

                //$("#cart-info-edit-status option[value='" + self.cart().current_status_id() + "']").attr("selected", "selected");
            });

        };

        self.saveAddress = function () {
            data = {customer_id: self.customer().customer_id(), house_number:self.location().house_number(),
                    street_name:self.location().street_name() +" "+ self.location().street_suffix(),
                    city:self.location().city(), state:self.location().state(), zipcode:self.location().zipcode(),
                     property_type: self.location().property_type(), geocode_status:self.location().geocode_status()};

            if (self.location().unit()) {
                data.unit = self.location().unit()
            }

            if (self.location().latitude()) {
                data.latitude = self.location().latitude();
            }

            if (self.location().longitude()) {
                data.longitude = self.location().longitude();
            }

            $.ajax(location_api_profile + 'New', {
                    data:ko.toJSON(data),
                    dataType:"jsonp",
                    type:"post", contentType:"application/json",
                    success:function (data) {
                        self.server_message_type(data.details.message_type);
                        self.server_message(self.server_message() + "<br>" + data.details.message);
                        //send message to last step
                        self.currentStep(self.stepModels()[self.stepModels().length - 1]);
                    },
                    error:function (jqXHR, status, error) {
                        //send error message to last step
                        self.currentStep(self.stepModels()[self.stepModels().length - 1]);
                        self.server_message_type("Failed");
                        self.server_message(jqXHR.statusText);

                    }

                }
            )

        };

       self.saveCustomer = function () {

           //#TODO improve this ... quick and dirty validation:


           if (self.location().zipcode() == 'Select One'){
               alert("Please Select a Zipcode");
               self.currentStep(self.stepModels()[1]);
               return;
           }


            data = ko.toJSON(self.customer);
            $.ajax(customer_api_url + 'New', {
                    data:data,
                    type:"post", contentType:"application/json",
                    dataType:"jsonp",
                    success:function (data) {
                        self.customer().customer_id(data.details.customer_id);
                        self.saveAddress();
                        self.server_message(data.details.message);
                    },
                    error:function (jqXHR, status, error) {
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
               if (self.currentStep().id == 3){
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

    }

    cartlogic.CustomerNewViewModel = CustomerNewViewModel


})(window.cartlogic);



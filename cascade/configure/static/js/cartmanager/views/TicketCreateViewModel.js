/**
 *
 * User: jbennett
 * Date: 3/3/13
 * Time: 10:38 PM
 *
 */


(function (cartlogic) {

    function TicketCreateViewModel() {

        var self = this;
        self.service_type_options = ko.observableArray(['Delivery', 'Exchange', 'Remove', 'Repair']);
        self.service_type = ko.observable("None");
        self.cart_serial_number = ko.observable(cart_serial_number);
        self.cartSerialList = ko.observableArray([]);
        self.service_charge = ko.observable(0.00);
        self.service_charge_options = ko.observableArray([]);

        //Use if cart id was sent from a cart profile page
        self.cart_id = ko.observable(cart_id);
        self.cart_address_search = ko.observable();

        //address info to send to the server
        self.cart_house_number = ko.observable(cart_address_house_number);
        self.cart_street_name = ko.observable(cart_address_street_name);
       // self.cart_street_suffix = ko.observable(cart_address_suffix);
       // self.cart_street_direction = ko.observable(cart_address_direction);
        self.cart_unit = ko.observable(cart_address_unit);
        self.cart_full_address = ko.observable(cart_full_address);

        self.selected_cart_parts = ko.observableArray([]);

        self.addressList = ko.observableArray([]);
        self.cart_size = ko.observable("");
        self.cart_type = ko.observable("None");
        self.cart_parts_options = ko.observableArray([]);
        self.cart_type_options = ko.observableArray([]);
        //get only the unique sizes from the cart type options
        self.cart_type_unique_sizes = ko.computed(
            function () {
                var sizes = ko.utils.arrayMap(self.cart_type_options(), function (item) {
                    return item.size;
                });

                return ko.utils.arrayGetDistinctValues(sizes).sort();
            }
        );

        //use the selected size (i.e. self.cart_size() to filter out the appropriate cart type names
        //For example only show
        self.cart_type_unique_type = ko.computed(
            function () {
                var types = ko.utils.arrayFilter(self.cart_type_options(), function(item) {
                    if (self.cart_size() == item.size) {
                        return item;
                    }
                });

                var names = ko.utils.arrayMap(types, function (item) {
                    return item.name
                });

                return names;
            }

        );

        self.server_message = ko.observable("None");
        self.server_message_type = ko.observable("None");

        self.stepModels = ko.observableArray([
            new cartlogic.FormStep(2, "Confirm Address", "ConfirmAddress", {message: ko.computed(function () {
                if (!self.cart_full_address()) {
                    return "<i class='text-error icon-2x icon-exclamation-sign'>GO BACK, NO ADDRESS FOUND<i>"
                }
                return "Please Confirm Your Address"

            })
            }),
            new cartlogic.FormStep(3, "Select Service Type", "SelectServiceType",
                {services: self.service_type_options, message: "Create New Service Ticket Wizard" }),
            new cartlogic.FormStep(7, "Confirm Ticket", "ConfirmTicket", {service_type: self.service_type(),
                serial_number: self.cart_serial_number(), address: self.cart_address_search(),
                cart_size: self.cart_size(), cart_type: self.cart_type(), message: 'Confirm Ticket'}),
            new cartlogic.FormStep(8, "Complete", "Complete", {message: "Ticket Request Completed"})

        ]);


        //check for cart address house number null if it is "null" then add address search at the beginning
        if (!cart_address_house_number) {
            var address_search_step = new cartlogic.FormStep(1, "Search Address", "SearchAddress",
                {message: ko.observable("Type Address below. Example: 201 Market Ave SE") });
            self.stepModels.splice(0, 0, address_search_step);
        }

        var cart_size_step = new cartlogic.FormStep(5, "Select Cart Size", "SelectCartSize", {
            cart_types: self.cart_type_unique_sizes,
            message: "Select a Cart Size" });

        var cart_type_step = new cartlogic.FormStep(6, "Select Cart Type", "SelectCartType", {
            cart_types: self.cart_type_unique_type,
            message: ko.computed(function () {
                    if (!self.cart_size()) {
                        return "<i class='text-error icon-2x icon-exclamation-sign'>GO BACK, SELECT A CART SIZE!</i>"
                    }
                    return "Select Cart type:"
                }

            ) });

        self.stepModels.splice(-2, 0, cart_size_step);
        self.stepModels.splice(-2, 0, cart_type_step);

        //call get service charge
        self.getServiceCharges = function(){
           $.getJSON(cart_service_charge_api_url, function(data){
               if (data.length){
                   var service_charge_step = new cartlogic.FormStep(9, "Select Service Charge", "SelectServiceCharge",{
                       service_charges: self.service_charges,
                       message: "Select a Service Charge"
                       });
                  self.stepModels.splice(-2, 0, service_charge_step);
                }
                var serviceChargesList = $.map(data, function(item){
                   return new cartlogic.ServiceCharge(item)
                });
               self.service_charge_options(serviceChargesList);
          });
        }

       self.getServiceCharges();

       //same logic in Cart Profile view model, only grabs all options
       self.getCartTypeOptions = function () {
            $.getJSON(cart_type_options_api_url, function (data) {
                    var cartTypeList = $.map(data, function (item) {
                        return  new cartlogic.CartTypeOption(item)
                    });
                    self.cart_type_options(cartTypeList);
               }
            )
        };

       self.getCartPartsOptions = function(){
           $.getJSON(cart_parts_api_url, function(data){
               var cartPartsList = $.map(data, function(item){
                   return new cartlogic.CartParts(item)
               });
               self.cart_parts_options(cartPartsList);
           });
       };

       self.getCartPartsOptions();

        self.getCartTypeOptions();

        self.set_address_cart_list = function (data, event) {
           self.cart_house_number(data.house_number());
           self.cart_street_name(data.street_name());
           self.cart_unit(data.unit());
          // self.cart_street_direction(data.direction());
          // self.cart_street_suffix(data.suffix());
           self.cart_full_address(data.full_address());
           if (data.carts().length) {
               self.cartSerialList(data.carts());
            }

            return true

        };

        //subscribe to the service type selected and update the wizard as needed:
        self.update_wizard = self.service_type.subscribe(function (service_type) {
            //replace service_type_options with service_type so we don't have to manage adding
            //removing the stepModels added for exchange or remove
            self.service_type_options([service_type]);
            if (service_type == 'Exchange' || service_type == 'Remove' || service_type == 'Repair') {
                if (!cart_serial_number) {
                    //check for serial, if null serial, then insert cart serial select
                    //the list of serial numbers comes from location query in self.searchAddress, Note the Click binding on address input
                    //from ticket_new.html
                    var serial_cart_select = new cartlogic.FormStep(4, "Select Cart Serial Number to <b>Remove " +
                        "Exchange or Repair</b>", "SelectSerial", {message: ko.observable("Select Cart Serial Number below")});
                    self.stepModels.splice(3, 0, serial_cart_select);

                } else {
                    // For tickets started from the Cart Profile Page
                    // Just need to confirm the cart serial number that was already sent to the page (i.e. global)
                    //so, we add a confirm step.
                    var confirm_cart_serial = new cartlogic.FormStep(4, "Confirm Cart Serial Number to " +
                        "<b> Remove or Exchange </b>", "ConfirmSerial", {message: ko.observable("Select Next to Confirm")});
                    self.stepModels.splice(2, 0, confirm_cart_serial);
                }
            if(service_type == 'Repair' || service_type == 'Remove'){

                self.stepModels.remove(function(item){
                    return item.id == 5 || item.id == 6;
                })

                if(service_type == 'Repair'){

                var parts_options_select = new cartlogic.FormStep(10, 'Select Parts', 'SelectParts',
                                                                 {message:"Select parts to be repaired"});
                self.stepModels.splice(-2, 0, parts_options_select);
                }
            }

            }

        });

        //Gets the typed address from the server
        self.searchAddress = function () {
            if (self.cart_address_search() && self.cart_address_search().length == 5) {

                var data = {"address": self.cart_address_search()};
                var message_index = ko.utils.arrayFirst(self.stepModels(), function (item) {
                    return item.id === 1
                });
                message_index.model().message('<span class="text-success">' + 'Loading...' + '</span>');
                //call server to get a list of addresses to select
                $.getJSON(location_api_search, data, function (data) {
                    var addressList = $.map(data, function (item) {
                        return new cartlogic.Location(item);
                    });

                    self.addressList(addressList);
                    //checking address lengths and adding the appropriate message
                    if (addressList.length == 0) {
                        message_index.model().message('<span class="text-error"> No Address Found! </span><br>' +
                            '<i class="text-info"> To add new, close this window and click on Customer >> New');
                    } else if (addressList.length == 1) {
                        message_index.model().message('<span class="text-success">' +
                            'Found one, please select and Click next' + '</span>');
                    } else {
                        message_index.model().message('<span class="text-success">' + '<b>Found ' +
                            addressList.length + '</b>... please select one and Click next' + '</span>');
                    }

                });

            }
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


        self.createNewTicket = function () {
            //If serial_number = new, then this function will create a new ticket
            var data = {'service_type': self.service_type(), 'house_number': self.cart_house_number(), 'street_name': self.cart_street_name()};

            if (self.cart_unit() && self.cart_unit() != " ") {
                //add the unit so we get a unique address
                //Note could have just sent back an address id, but want to stay away from system ids (fear they could
                //change)
                data.address_unit = self.cart_unit();
            }

/*            if (self.cart_street_suffix() && self.cart_street_suffix() != " "){
                data.street_suffix = self.cart_street_suffix();
            }*/

/*            if (self.cart_street_direction() && self.cart_street_direction() != " "){
                data.street_direction = self.cart_street_direction();
            }*/

            if (self.service_type() == 'Delivery' || self.service_type() == 'Exchange') {
                data.cart_size = self.cart_size();
                data.cart_type = self.cart_type();
            }

            if (self.service_type() != 'Delivery') {
                data.cart_serial_number = self.cart_serial_number();
            }

            if (self.service_type() != 0.00) {
                data.service_charge = self.service_charge();
            }

            if (self.selected_cart_parts().length > 0){
                data.cart_parts = self.selected_cart_parts();
            }

            $.ajax(ticket_api + 'New', {
                    data: ko.toJSON(data),
                    type: "post", contentType: "application/json",
                    dataType: "jsonp",
                    success: function (data) {
                        self.server_message_type(data.details.message_type);
                        self.server_message(data.details.message);
                        //send message to last step
                        self.currentStep(self.stepModels()[self.stepModels().length - 1]);
                    },

                    error: function (jqXHR, status, error) {
                        //send error message to last step
                        self.currentStep(self.stepModels()[self.stepModels().length - 1]);
                        self.server_message_type("FAILED");
                        self.server_message(jqXHR.statusText);
                    }
                }

            )

        };

    }

    cartlogic.TicketCreateViewModel = TicketCreateViewModel;

})(window.cartlogic);
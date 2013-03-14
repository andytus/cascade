/**
 *
 * User: jbennett
 * Date: 3/3/13
 * Time: 10:38 PM
 *
 */


(function (cartlogic) {

    function TicketCreateViewModel() {

        self = this;
        self.service_type_options = ko.observableArray(['Delivery', 'Exchange', 'Remove']);
        self.service_type = ko.observable("None");
        self.serial_number = ko.observable(serial_number);
        //Use if cart id was sent from a cart profile page
        self.cart_id = ko.observable(cart_id);
        self.cart_address = ko.observable(cart_address);
        self.full_address = ko.observable("None");
        self.cart_size = ko.observable("");
        self.cart_type = ko.observable("None");
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
        self.cart_type_unique_type = ko.computed(
            function () {
                var types = ko.utils.arrayFilter(self.cart_type_options(), function (item) {
                    if (self.cart_size() == item.size) {
                        return item
                    }
                    // return ko.utils.stringStartsWith(item.size, self.cart_size())

                });
                var names = ko.utils.arrayMap(types, function (item) {
                    return item.name
                });
                return names;
            }

        );

        self.server_message = ko.observable("None");

        //Duplicated from LocationSearchViewModel in order to accommodate wizard steps for searching for an address

        self.selected_address = ko.observable("");
        self.addresses = ko.observableArray([]);

        self.stepModels = ko.observableArray([
            new cartlogic.FormStep(2, "Confirm Address", "ConfirmAddress", {message:
                ko.computed(function(){
                    if (!self.cart_address()){
                        return "<i class='text-error icon-2x icon-exclamation-sign'>GO BACK, NO ADDRESS FOUND<i>"
                    }
                    return "Please Confirm Your Address"

                })
            }),
            new cartlogic.FormStep(3, "Select Service Type", "SelectServiceType", {services:self.service_type_options, message:"Create New Service Ticket Wizard" }),
            new cartlogic.FormStep(7, "Confirm Ticket", "ConfirmTicket", {service_type:self.service_type(), serial_number:self.serial_number(), address:self.full_address(),
                cart_size:self.cart_size(), cart_type:self.cart_type(), message:'Confirm Ticket'}),
            new cartlogic.FormStep(8, "Complete", "Complete", {message:"DONE..Put All values here"})
        ]);


        //check for cart address null if it is "null" then add address search at the beginning
        if (!cart_address) {
            var address_search_step = new cartlogic.FormStep(1, "Search Address", "SearchAddress",
                {address:self.cart_address, message:ko.observable("Type Address below. Example: 201 Market Ave SE") });
            self.stepModels.splice(0, 0, address_search_step);
        }

        var cart_size_step =  new cartlogic.FormStep(5, "Select Cart Size", "SelectCartSize", {
            cart_types: self.cart_type_unique_sizes,
            message:"Select a Cart Size" });

        var cart_type_step =  new cartlogic.FormStep(6, "Select Cart Type", "SelectCartType", {
            cart_types:self.cart_type_unique_type,
            message:ko.computed( function(){
                   if (!self.cart_size()){
                       return "<i class='text-error icon-2x icon-exclamation-sign'>GO BACK, SELECT A CART SIZE!</i>"
                   }
                   return "Select Cart type:"
                }

            ) });//#todo put a computeed obserable for the message ... i.e. if size is not selected ... say u must!

        self.stepModels.splice(-2, 0, cart_size_step);
        self.stepModels.splice(-2, 0, cart_type_step);


        //same logic in Cart Profile view model, only grabs all options
        self.getTypeOptions = function () {
            $.getJSON(cart_type_api, function (data) {
                    var cartTypeList = $.map(data, function (item) {
                        return  new cartlogic.TypeOption(item)
                    });
                    self.cart_type_options(cartTypeList);
                }
            )
        };

        self.getTypeOptions();


        self.update_wizard = self.service_type.subscribe(function(service_type) {
            if (service_type == 'Exchange' || service_type == 'Remove') {
                if (!serial_number) {
                    //check for serial ... if null serial, then insert cart serial search step
                    //serial search step only used for remove or exchange without serial numbers
                    var serial_cart_search = new cartlogic.FormStep(4, "Select Cart Serial Number", "SearchSerial", {message:ko.observable("Type Cart Serial Number below")});
                    self.stepModels.splice(3, 0, serial_cart_search);
                    //remove cart size and step for Remove tickets ...not needed

                }
                if (service_type == 'Remove'){
                    self.service_type_options.remove('Delivery');
                    self.service_type_options.remove('Exchange');
                    self.stepModels.remove(cart_size_step);
                    self.stepModels.remove(cart_type_step);
                } else{
                    self.service_type_options.remove('Remove');
                    self.service_type_options.remove('Delivery');
                }

           } else{
                //this is a Delivery remove the Exchange and Remove
                self.service_type_options.remove('Exchange');
                self.service_type_options.remove('Remove');

            }

        });


        //gets the typed address from the server
        //Not very DRY, repeated slightly different in several view models for expediency
        self.searchAddress = function () {
            if (self.cart_address() && self.cart_address().length == 5) {

                data = {"address":self.cart_address()};

                message_index = ko.utils.arrayFirst(self.stepModels(), function (item) {
                    return item.id === 1
                });

                message_index.model().message('<span class="text-success">' + 'Loading...' + '</span>');

                $.getJSON(location_api_search, data, function (data) {

                    var addressList = $.map(data.results, function (item) {
                        return new cartlogic.Location(item);
                    });

                    self.addresses(addressList);

                    //checking address lengths and adding the appropriate message
                    if (addressList.length == 0) {
                        message_index.model().message('<span class="text-error"> No Address Found! </span><br><i class="text-info"> To add new, close this window and click on Customer >> New');
                        console.log(message_index.model().message)
                    } else if (addressList.length == 1) {
                        message_index.model().message('<span class="text-success">' + 'Found one, please select and Click next' + '</span>');
                        console.log(message_index.model().message)
                    } else {
                        message_index.model().message('<span class="text-success">' + '<b>Found ' + addressList.length + '</b>... please select one and Click next' + '</span>');
                    }

                });

            }
        };



        //Wizard Step Navigation

        self.currentStep = ko.observable(self.stepModels()[0]);

        self.currentIndex = ko.computed(function () {
            console.log(self.stepModels.indexOf(self.currentStep()));
            return self.stepModels.indexOf(self.currentStep());
        });

        self.isConfirmStep = ko.computed(function () {
            return self.currentIndex() == self.stepModels().length - 2;

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
            return self.currentIndex() > 0;
        });

        self.goPrevious = function () {
            if (self.canGoPrevious()) {
                self.currentStep(self.stepModels()[self.currentIndex() - 1]);
            }
        };

        //used when cart serial is not provided on an Exchange or Removal Service
        self.getCartData = function (data) {

        };

        self.updateAddress = function () {
            // update from wizard
        };


        self.createNewTicket = function (serial_number) {
            //Note: if serial_number = new, then this function will create a new ticket
            //#TODO working on creating a ticket
            //#TODO Should do validation before sending to server, if any of the above observables where not completed ,... return fix first


            $.ajax(ticket_api + serial_number, {
                    data:ko.toJSON({'test':"foo me"}),
                    type:"post", contentType:"application/json",
                    dataType:"jsonp"
                }

            )

        };

    }

    cartlogic.TicketCreateViewModel = TicketCreateViewModel;

})(window.cartlogic);
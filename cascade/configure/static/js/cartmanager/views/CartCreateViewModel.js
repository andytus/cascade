/**
 *
 * User: jbennett
 * Date: 9/14/13
 * Time: 9:34 PM
 *
 */


(function (cartlogic) {

    function CartCreateViewModel(cart_api_profile_url, cart_type_options_api_url) {
        var self = this;
        self.server_message = ko.observable();
        self.server_message_type = ko.observable();

        self.cart_serial_number = ko.observable();
        self.serial_good = ko.observable(false);
        self.cart_serial_check_message = ko.observable();

        self.cart_size = ko.observable();
        self.cart_type = ko.observable();
        self.cart_born_date = ko.observable();

        //#TODO <----The following is not DRY, repeated in TicketCreateViewModel. Should be parsed to its own view model---->
        self.cart_type_options = ko.observableArray([]);

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
                var types = ko.utils.arrayFilter(self.cart_type_options(), function (item) {
                    if (self.cart_size() == item.size) {
                        return item
                    }
                });
                var names = ko.utils.arrayMap(types, function (item) {
                    return item.name
                });
                return names;
            }
        );

        //same logic in CartProfileViewModel & TicketCreateViewModel view model, only grabs all options
        self.getCartTypeOptions = function () {

            $.getJSON(cart_type_options_api_url, function (data) {
                    var cartTypeList = $.map(data, function (item) {
                        return  new cartlogic.CartTypeOption(item)
                    });
                    self.cart_type_options(cartTypeList);
                }
            )
        };

        self.getCartTypeOptions();

        self.cartSerialLookup = function () {
            if (self.cart_serial_number() && self.cart_serial_number().length > 7) {
                if (self.cart_serial_number().length > 30) {
                    //validate not larger than 30
                    self.serial_good(false);
                } else {
                    $.ajax(cart_api_profile_url + self.cart_serial_number(), {
                        type: "get", contentType: "application/json",
                        dataType: "jsonp",
                        success: function (data) {
                            if (data.serial_number.length) {
                                //validate cart does not exist
                                self.serial_good(false)
                                self.cart_serial_check_message("Cart exist!")
                            }
                        },
                        error: function (jqXHR, status) {
                            if (jqXHR.status == 404) {
                                //cart does not exist
                                self.serial_good(true);
                                self.cart_serial_check_message("Good!")
                            }
                        }
                    })

                }

            } else {
                //if the serial number length is not correct then its invalid
                self.serial_good(false)
                self.cart_serial_check_message("")
            }

        }


        self.createNewCart = function () {
            var url = cart_api_profile_url + self.cart_serial_number();
            console.log(self.cart_type());
            var data = {'create_new': true, 'cart_type__name': self.cart_type(), 'cart_type__size': self.cart_size()};

            if (self.cart_born_date()) {
                data.born_date = self.cart_born_date();
            }

            $.ajax(url, {
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

            });
        }


        self.stepModels = ko.observableArray([ new cartlogic.FormStep(1, 'Cart Serial Number', 'EnterCartSerial', {message: 'Enter Cart Serial Number'}),
            new cartlogic.FormStep(2, 'Cart Size', 'SelectCartSize', {message: 'Select Cart Size'}),
            new cartlogic.FormStep(3, 'Cart Type', 'SelectCartType', {message: 'Select Cart Type'}),
            new cartlogic.FormStep(3, 'Cart Produced Date', 'SelectBornDate', {message: 'Enter Cart Produced Date'}),
            new cartlogic.FormStep(4, 'Confirm', 'ConfirmCartSave', {message: '<b>Confirm & Save Cart<b>'}),
            new cartlogic.FormStep(5, 'Complete', 'Complete', {message: 'Complete'}),
        ]);

        self.addCalendar = function () {
            // hack to add date picker for born date here, ugly but works
            if (self.currentIndex() == 3) {
                //putting in a date and time picker
                $('#datepicker').datepicker({
                    format: 'mm-dd-yyyy'
                });
            }
        }


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
            self.addCalendar();
        };

        self.canGoPrevious = ko.computed(function () {
            //can go to previous if the index is greater than zero and less than the last step (i.e. success)
            return self.currentIndex() > 0 && self.currentIndex() < self.stepModels().length - 1;
        });

        self.goPrevious = function () {
            if (self.canGoPrevious()) {
                self.currentStep(self.stepModels()[self.currentIndex() - 1]);
            }
            self.addCalendar();
        };

    }

    cartlogic.CartCreateViewModel = CartCreateViewModel


})(window.cartlogic);
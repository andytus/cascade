/**
 *
 * User: jbennett
 * Date: 3/19/13
 * Time: 2:46 PM
 *
 */


(function (cartlogic) {

    function CartProfileChangeAddressViewModel() {

        var self = this;
        //get serial number from global
        self.cart_serial = ko.observable(serial_number);
        self.address_id = ko.observable(null);
        self.server_message_type = ko.observable();
        self.server_message = ko.observable();


        self.setAddressId = function(){
            self.address_id(this.id());
        };


        self.stepModels = ko.observableArray([

            new cartlogic.FormStep(1, "Confirm Serial", "ConfirmSerial",
                {cart_serial:self.cart_serial, message:"Are you sure you want to change the address for <b>" + self.cart_serial() + "</b>?<br> <br><b>Note:</b> " +
                    "<i>This will <u>not</u> create a service ticket and" +
                    " will update both the <u>coordinates</u> and <u>address</u>." +
                    " <br><br> Click next to continue.</i>"}),

            new cartlogic.FormStep(2, "Search for New Address", "SearchAddress", {message:"Type Address below. Example: 201 Market Ave SE" }),

            new cartlogic.FormStep(3, "Confirm Cart Address Change", "ConfirmAddressChange", {message: "Click <u>save changes</u> to change cart<b> " +self.cart_serial() +"</b> to:"}),
            new cartlogic.FormStep(4, "Cart Address Change Request Completed", 'Complete', {message: "Click on close to return to the Cart Profile"})

        ]);


        self.saveCartAddress = function(){
            var data = {"location_id": self.address_id()};
            $.ajax(cart_api_profile + serial_number, {
                data:ko.toJSON(data),
                type:"post", contentType:"application/json",
                dataType:"jsonp",
                success:function (data) {
                    self.server_message_type(data.details.message_type);
                    self.server_message(data.details.message);
                    //send message to last step
                    self.currentStep(self.stepModels()[self.stepModels().length-1]);
                },
                error:function (data) {
                    //send error message to last step
                    self.currentStep(self.stepModels()[self.stepModels().length-1]);
                    self.server_message_type("ERROR!");
                    self.server_message(jqXHR.statusText)
                }
            })
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
            //can go to previous if the index is greater than zero.
            return self.currentIndex() > 0 && self.currentIndex() < self.stepModels().length -1;
        });

        self.goPrevious = function () {
            if (self.canGoPrevious()) {
                self.currentStep(self.stepModels()[self.currentIndex() - 1]);
            }


        }

    }


   cartlogic.CartProfileChangeAddressViewModel = CartProfileChangeAddressViewModel;


})(window.cartlogic);

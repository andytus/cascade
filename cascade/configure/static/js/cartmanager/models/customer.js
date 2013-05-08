/**
 *
 * User: jbennett
 * Date: 3/23/13
 * Time: 11:13 AM
 *
 */


(function (cartlogic) {

    function Customer(data) {

        var self = this;
        self.customer_id = ko.observable("");
        self.first_name = ko.observable(" ").extend({ validate: {required: true,  requiredMessage: "Please enter a first name"} });
        self.last_name = ko.observable(" ").extend({ validate: {required: true, requiredMessage: "Please enter a last name"} });
        self.phone_number = ko.observable("").extend({validate:{required: false, pattern: "phone"}});
        self.email = ko.observable("").extend({validate:{required: false, pattern: 'email'}});

        self.valid = ko.computed(function(){
          return !(self.first_name.hasError())
                 && !(self.last_name.hasError())
                 && !(self.phone_number.hasError())
                 && !(self.email.hasError())

        });

     // if data was sent then initialize values below
      if (data) {
          self.customer_id(data.id);
          self.first_name(data.first_name);
          self.last_name(data.last_name);
          self.phone_number(data.phone_number);
          self.email(data.email);


      }

    }

    cartlogic.Customer = Customer;

})(window.cartlogic);
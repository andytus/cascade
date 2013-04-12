/**
 *
 * User: jbennett
 * Date: 3/23/13
 * Time: 11:13 AM
 *
 */


(function (cartlogic) {

    function CustomerProfileViewModel() {

        var self = this;
        self.customer = ko.observable();
        self.customer_id = ko.observable(customer_id);
        self.edit_customer = ko.observable(false);
        self.customer_addresses = ko.observableArray([]);

        self.removeAddressId = ko.observable("");

        self.getCustomerData = function(){
            $.ajax({

                url: customer_api_url + self.customer_id(),
                type: 'GET',
                dataType: "json",
                success: function(data){
                     self.customer(new cartlogic.Customer(data));
                },
                error: function(data){
                    $("#message").removeClass("alert-info").addClass("alert-error").html("Error:" + data.statusText).show();
                }
            });

        };

        //#TODO verify/data chekc here, return true or apply error message, and false
        self.checkCustomerData = function(){};

        self.saveCustomerData = function(){

             //grab changes
             data = ko.toJSON({customer_id: self.customer_id(), first_name: self.customer().first_name(),
                              last_name: self.customer().last_name(), phone_number: self.customer().phone_number,
                              email: self.customer().email()});

            $.ajax({
                url: customer_api_url + self.customer_id(),
                type: 'POST',
                data: data,
                dataType: "json",
                success: function(data){
                    $("#message-type").text(data.details.message_type +"! ");
                    $("#message-text").text(data.details.message);
                    $('.close').click(function () {
                        $('#message').hide();
                    });
                    if (data.details.message_type == 'Success'){
                        $("#message").removeClass("alert-error").addClass('alert-success').show();
                    } else{
                        $("#message").removeClass("alert-success").addClass('alert-error').show();
                    }
                },
                error: function(data){
                    $("#message").removeClass("alert-info").addClass("alert-error").html("Error:" + data.statusText).show();
                }

            })


        };


        self.getAddresses = function(){
         //#TODO get the address using customer_id
         data = {customer_id: customer_id};
            $.ajax({
                url: location_api_search,
                type: "GET",
                data: data,
                dataType: "json",
                success: function(data){
                    //#TODO create and array of address
                    var addressList = $.map(data, function(item){
                        return new cartlogic.Location(item)

                    });
                    self.customer_addresses(addressList);
                }

            });
       };

       self.removeFromAddresses = function(){
          self.customer_addresses.remove(
              function(item){
                  return item.id() == self.removeAddressId()
              }
          )
       };

       self.confirmRemoveAddress = function(){
       $("#remove_confirm_address").html("<p>Are you sure you want to remove "+ this.full_address()+" ?</p>");
       $("#remove_confirm").modal('show');
       self.removeAddressId(this.id());
       };

       self.removeAddress = function(){
           data = ko.toJSON({customer_id:self.customer_id(), operation: 'remove'});
           $.ajax({
               url: location_api_profile + self.removeAddressId(),
               type: "POST",
               data: data,
               dataType: "json",
               success: function (data){
                   $("#message-type").text(data.details.message_type +"! ");
                   $("#message-text").text(data.details.message);
                   $('.close').click(function () {
                       $('#message').hide();
                   });
                   if (data.details.message_type == 'Success'){
                       $("#message").removeClass("alert-error").addClass('alert-success').show();
                       //simple remove from the addresses array so the user doesn't see it anymore, clean up
                       self.removeFromAddresses();
                   } else{
                       $("#message").removeClass("alert-success").addClass('alert-error').show();
                   }

                   $("#remove_confirm").modal('hide');
               },
             error: function(data){
                 $("#message").removeClass("alert-info").addClass("alert-error").html("Error:" + data.statusText).show();
                 $("#remove_confirm").modal('hide');
             }

           });
       };


       self.allowEdit = function(){
            self.edit_customer(true);
        };


      //Call getCustomerData
        self.getCustomerData();
        self.getAddresses();

    }



    cartlogic.CustomerProfileViewModel = CustomerProfileViewModel;

})(window.cartlogic);
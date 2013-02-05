/**
 * User: joe.bennett
 * Date: 12/22/12
 * Time: 12:16 AM
 * To change this template use File | Settings | File Templates.
 */
//last_latitude: "0",
//    last_longitude: "0",
//    rfid: "121016134330111111111111",
//    serial_number: "1111112",
//    size: 96,
//    current_status: "test",
//    cart_type: "Recycle",
//    last_updated: "2012-12-08T15:33:03.147Z",
//    born_date: "2012-10-07T04:00:00Z"



function Location(data){
    this.id = ko.observable(data.id);
    this.house_number = ko.observable(data.house_number);
    this.street_name = ko.observable(data.street_name);
}

function StatusOption(data){
    this.id = ko.observable(data.id);
    this.level = ko.observable(data.level);
    this.label = ko.observable(data.label);
}

function TypeOption(data){
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
    this.size = ko.observable(data.size);
    this.site = ko.observable(data.site);
}


function CartProfileViewModel() {

    var self = this;

    self.last_longitude = ko.observable();
    self.last_latitude = ko.observable();
    self.rfid = ko.observable("");
    self.serial_number = ko.observable(serial_number);

    self.id = ko.observable("");
    self.cart_profile_url = ko.computed(function(){return cart_app_url + serial_number});
    self.size = ko.observable("");
    self.cart_type = ko.observable("");
    self.cart_type_id = ko.observable("");
    self.last_updated = ko.observable("");
    self.born_date = ko.observable("");
    //location information
    self.location_house_number = ko.observable("");
    self.location_street_name = ko.observable("");
    self.location_unit = ko.observable("");
    self.location_address = ko.computed(function(){
        address = self.location_house_number() + " " + self.location_street_name();
        if (self.location_unit()){
            address = address + " Unit: " + self.location_unit();
        }
        return address});
    self.location_latitude = ko.observable();
    self.location_longitude = ko.observable();
    self.location_type = ko.observable();

    //customer information
    self.customer_id = ko.observable();
    self.customer_name = ko.observable();
    self.customer_url = ko.computed(function(){return customer_app_url + self.customer_id()});


    //status information
    self.current_status_id = ko.observable();
    self.current_status = ko.observable();
    self.current_status_level = ko.observable();
    self.cart_status_options = ko.observableArray([]);
    self.changeCartStatus = ko.computed(function(){
        //#TODO Got to be a cleaner way
           $('#cart-info-edit-status').change(function() {
            var status = $("#cart-info-edit-status option:selected");
            self.current_status(status.text());
            level = self.cart_status_options();
            var match = ko.utils.arrayFirst(self.cart_status_options(), function(item) {
                return status.val() == item.id();
            });

            self.current_status_level(match.level())

        });

     //type information
    self.cart_type_options = ko.observableArray([]);
    self.changeCartType = ko.computed(function(){
       $('#cart-info-edit-type').change(function(){
           var type =  $('#cart-info-edit-type option:selected').text();
           self.cart_type(type);
       })
    });

    });


    self.getCartData = function () {
        $.getJSON(cart_api_url + serial_number, function (data) {

            self.id(data.id);
            self.rfid(data.rfid);
            self.size(data.cart_type.size);
            self.cart_type(data.cart_type.name);
            self.cart_type_id(data.cart_type.id);
            self.last_updated(new Date(data.last_updated).toDateString());
            self.born_date(new Date(data.born_date).toDateString());

            //location information
            self.location_house_number(data.location.house_number);
            self.location_street_name(data.location.street_name);
            self.location_unit(data.location.unit);
            self.location_latitude(data.location.latitude);
            self.location_longitude(data.location.longitude);
            self.location_type(data.location.type);

            //customer information
            self.customer_name(data.location.customer.info.name);
            self.customer_id(data.location.customer.info.id);

            //status information
            self.current_status_id(data.current_status.id);
            self.current_status_level(data.current_status.level);
            self.current_status(data.current_status.label);

            //Calling to get cart type options for this cart
            //filters based on size and needs to get the size from the current cart size
            self.getTypeOptions();
            //Calling to get the cart status options
            self.getStatusOptions();
            //Calling to get the tickets for this cart
            self.getTickets();

             //Set Default option for status change
            $("select option[value='" + self.current_status_id() + "']").attr("selected","selected");
            $("select option[value='" + self.cart_type_id() + "']").attr("selected","selected");
        })
    };

    self.getStatusOptions = function(){
        $.getJSON(cart_status_options_api_url, function(data){
               var cartStatusOptions = $.map(data, function(item){
                   return new StatusOption(item);
               });
             self.cart_status_options(cartStatusOptions);

        })
     };

    self.getTypeOptions = function(){
        url = cart_type_options_api_url + "?format=jsonp&callback=?";
        data = {'size': self.size()};
        $.getJSON(url, data, function(data){
            var cartTypeOptions = $.map(data, function(item){
                return new TypeOption(item)
            });
            self.cart_type_options(cartTypeOptions);
        });
    };

    self.saveCartData = function (){
        $.ajax(cart_api_url + serial_number, {
          data: ko.toJSON({current_status: self.current_status, cart_type: document.getElementById('cart-info-edit-type').value}),
          type: "post", contentType: "application/json",
          dataType: "jsonp",
          success: function(result){
              console.log(result.time);
              self.last_updated(new Date(result.time).toDateString());
              $("#message").addClass("alert-success").show();
              $("#message-type").text("Success! ");
              $("#message-text").text(result.message);
              $('.close').click(function() {
                  $('#message').hide();
              })

          },
          error: function(result){console.log(result)}
        })


    };


    self.getTickets = function(){
        //uses dataTables to populate the tickets table

           $('#ticket_table').dataTable( {
              // "bPaginate": false,
               "bLengthChange": false,
               "bFilter": true,
              // "bSort": false,
              // "bInfo": false,
               "bAutoWidth": true,
               // "bProcessing": true,
               //"bServerSide": true,
                "sAjaxSource": tickets_api_download,
                "sAjaxDataProp": "tickets",

               "sPaginationType": "bootstrap",
               "oLanguage": {
                   "sLengthMenu": "_MENU_ records per page"
               },


                "aoColumns": [
                   { "mData": "status" },
                   { "mData": "service_type" },
                   { "mData": "success_attempts" },
                   { "mData": "date_created", "sType": "date" },
                   { "mData": "date_last_accessed"},
                   { "mData": "house_number" },
                   { "mData": "street_name"},
                   { "mData": "unit"},
                   { "mData": "removed_cart"},
                   { "mData": "delivered_cart"},
                   { "mData": "audit_cart"}

               ],

               "fnServerData": function( sUrl, aoData, fnCallback, oSettings ) {
                   oSettings.jqXHR = $.ajax( {
                       "url": sUrl,
                       "data":{"cart_id":self.id()},
                       "success": fnCallback,
                       "dataType": "jsonp",
                       "cache": false
                   } );}

            } );


           };




    self.getLocation = function (){

    };

    self.updateLocation = function (){

    };

    //call the api to get the data on load
    self.getCartData();

}


$(document).ready(function(){
    ko.applyBindings(new CartProfileViewModel(), document.getElementById("cart_profile"))
    }
);



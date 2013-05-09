/**
 *
 * User: jbennett
 * Date: 5/7/13
 * Time: 10:04 PM
 *
 */


(function (cartlogic){

    function TicketsReportViewModel(data) {
        var self = this;

        self.selected_type = ko.observable();
        self.selected_status = ko.observable();
        self.selected_cart_type = ko.observable();
        self.selected_cart_size = ko.observable();

        //options for select drop downs
        self.ticket_type_options = ko.observableArray([]);
        self.ticket_status_options = ko.observableArray([]);
        self.cart_type_options = ko.observableArray([]);
        self.cart_size_options = ko.observableArray([]);


        self.getServiceTypeOptions = function(){
            $.getJSON(ticket_service_type_api, function(data){
                var serviceTypeOptions = $.map(data, function(item){
                    return item.service
                });
                self.ticket_type_options(serviceTypeOptions);
                self.ticket_type_options.unshift('ALL');
                var type_match = ko.utils.arrayFirst(self.ticket_type_options(), function(item){
                    return item == 'ALL'
                });

                self.selected_type(type_match);


            });
        };


        self.getServiceStatusOptions = function(){
            $.getJSON(ticket_status_api, function(data){
                var ticketStatusOptions = $.map(data, function (item) {
                    return item.service_status;
                });
                self.ticket_status_options(ticketStatusOptions);
                var match = ko.utils.arrayFirst(self.ticket_status_options(), function(item) {
                    return item === 'Requested';
                });
                self.selected_status(match);

            });
        };

       self.getCartTypeOptions = function () {
               url = cart_type_api + "?format=jsonp&callback=?";
               $.getJSON(url, data, function (data) {
                   var cartTypeOptions = $.map(data, function (item) {
                       return item.name
                   });
                   var cartSizeOptions = $.map(data, function (item) {
                       return item.size

                   });
                   self.cart_type_options(cartTypeOptions);
                   self.cart_size_options(cartSizeOptions);
                   self.cart_type_options.unshift('ALL');
                   self.cart_size_options.unshift('ALL');

                   var size_match = ko.utils.arrayFirst(self.cart_size_options(), function(item){
                      return item == 'ALL'
                   });

                   self.selected_cart_size(size_match);


                   var type_match = ko.utils.arrayFirst(self.cart_type_options(), function(item){
                       return item == 'ALL'
                   });
                   self.selected_cart_type(type_match);
             });
           };

        self.getServiceTypeOptions();
        self.getServiceStatusOptions();
        self.getCartTypeOptions();





    }
    cartlogic.TicketsReportViewModel = TicketsReportViewModel;

})(window.cartlogic);
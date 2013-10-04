/**
 *
 * User: jbennett
 * Date: 10/2/13
 * Time: 10:41 AM
 *
 */


(function(cartlogic){

    function Route(data){
       var self = this;
       self.id = ko.observable();
       self.route = ko.observable();
       self.route_day = ko.observable();
       self.route_type = ko.observable();

       if (data){
           self.id(data.id);
           self.route(data.route);
           self.route_day(data.route_day);
           self.route_type(data.route_type);
       }

    }

    cartlogic.Route = Route;

 }

)(window.cartlogic);
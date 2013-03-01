/**
 *
 * User: jbennett
 * Date: 2/27/13
 * Time: 10:53 AM
 *
 */


/* Defined Name Space */


window.cartlogic = {};

(function(cartlogic){

  function App(){
       this.cart_list = function(element){
       var cart_list = new cartlogic.CartsListViewModel();
       ko.applyBindings(cart_list, element);
       };

      this.cart_search = function(element){
      var cart_search = new cartlogic.CartSearchViewModel();
      ko.applyBindings(cart_search, element);
      };

      this.cart_profile = function(element){
      var car_profile = new cartlogic.CartProfileViewModel();
      ko.applyBindings(cart_profile, element);
      };

      this.ticket_list = function(element){
      var ticket_list = new cartlogic.TicketsViewModel();
      ko.applyBindings(ticket_list, element);
      };

  }
    cartlogic.App = App;

}(window.cartlogic));

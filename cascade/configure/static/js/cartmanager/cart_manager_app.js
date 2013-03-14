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

      this.cart_search = function(){
        var cart_search = new cartlogic.CartSearchViewModel();
        ko.applyBindings(cart_search);

      };

      this.cart_profile = function(){
      var cart_profile = new cartlogic.CartProfileViewModel();
      ko.applyBindings(cart_profile);
      };

      this.ticket_list = function(){
      var ticket_list = new cartlogic.TicketsViewModel();
      ko.applyBindings(ticket_list);
      };

  }
    cartlogic.App = App;

}(window.cartlogic));

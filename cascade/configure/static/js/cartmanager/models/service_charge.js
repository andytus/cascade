/**
 *
 * User: jbennett
 * Date: 11/12/13
 * Time: 1:54 PM
 *
 */



(function (cartlogic){

    function ServiceCharge(data){

    var self = this;
    self.id =data.id;
    self.amount = data.amount;
    self.currency = data.currency;
    self.description = data.description;
    }

//add to cartlogic name space
    cartlogic.ServiceCharge = ServiceCharge ;

}(window.cartlogic));

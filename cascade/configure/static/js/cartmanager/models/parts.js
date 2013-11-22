/**
 *
 * User: jbennett
 * Date: 11/19/13
 * Time: 11:41 AM
 *
 */


(function (cartlogic){

    function CartParts(data) {
        this.id = data.id;
        this.name = data.name;
        this.description = data.description;
        this.on_hand = data.on_hand;
    }
    cartlogic.CartParts = CartParts;

})(window.cartlogic);
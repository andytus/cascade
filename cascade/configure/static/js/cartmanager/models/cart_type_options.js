/**
 *
 * User: jbennett
 * Date: 3/3/13
 * Time: 6:34 PM
 *
 */


(function (cartlogic){

    function CartTypeOption(data) {
        this.id = data.id;
        this.name = data.name;
        this.size = data.size;
        this.site =data.site;
    }
    cartlogic.CartTypeOption = CartTypeOption;

})(window.cartlogic);
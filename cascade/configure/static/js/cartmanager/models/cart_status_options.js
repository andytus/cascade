/**
 *
 * User: jbennett
 * Date: 3/3/13
 * Time: 6:34 PM
 *
 */



(function (cartlogic) {

    function CartStatusOptions(data) {
        var self = this;
        self.id = ko.observable(data.id);
        self.level = ko.observable(data.level);
        self.label = ko.observable(data.label);

    }

    cartlogic.CartStatusOptions = CartStatusOptions;

})(window.cartlogic);
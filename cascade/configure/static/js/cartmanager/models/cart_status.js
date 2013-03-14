/**
 *
 * User: jbennett
 * Date: 3/3/13
 * Time: 6:34 PM
 *
 */



(function (cartlogic){

    function StatusOption(data) {
        this.id = ko.observable(data.id);
        this.level = ko.observable(data.level);
        this.label = ko.observable(data.label);
    }

   cartlogic.StatusOption = StatusOption;


})(window.cartlogic);
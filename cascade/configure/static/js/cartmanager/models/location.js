/**
 *
 * User: jbennett
 * Date: 3/3/13
 * Time: 6:34 PM
 *
 */


(function (cartlogic){

    function Location(data) {
        this.id = ko.observable(data.id);
        this.house_number = ko.observable(data.house_number);
        this.street_name = ko.observable(data.street_name);
    }

    cartlogic.Location = Location;

})(window.cartlogic);

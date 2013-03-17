/**
 *
 * User: jbennett
 * Date: 3/3/13
 * Time: 6:34 PM
 *
 */


(function (cartlogic){

    function Location(data) {
        this.id = ko.observable(data.info.properties.id);
        this.house_number = ko.observable(data.info.properties.house_number);
        this.street_name = ko.observable(data.info.properties.street_name);
        this.unit = ko.observable(data.info.properties.unit);
        console.log(this.unit());
        this.carts = ko.observableArray(data.info.properties.carts);
    }

    cartlogic.Location = Location;

})(window.cartlogic);

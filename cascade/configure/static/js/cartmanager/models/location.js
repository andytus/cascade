/**
 *
 * User: jbennett
 * Date: 3/3/13
 * Time: 6:34 PM
 *
 */


(function (cartlogic){

    function Location(data) {
        var self = this;
        self.id = ko.observable(data.info.properties.id);
        self.house_number = ko.observable(data.info.properties.house_number);
        self.street_name = ko.observable(data.info.properties.street_name);
        self.unit = ko.observable(data.info.properties.unit);
        self.full_address = ko.computed(function(){
            var full_address = self.house_number() + " "+ self.street_name();
            if (self.unit()){
                full_address = full_address + " " + self.unit();
            }
            return full_address;
        });
        self.carts = ko.observableArray(data.info.properties.carts);
    }

    cartlogic.Location = Location;

})(window.cartlogic);

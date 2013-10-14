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
        self.id = ko.observable();
        self.property_type = ko.observable();
        self.house_number = ko.observable().extend({ validate: {required: true,  requiredMessage: "Missing house number"} });
        self.street_name = ko.observable().extend({ validate: {required: true,  requiredMessage: "Need a street"} });
        self.street_suffix = ko.observable("");
        self.unit = ko.observable();
        self.full_address = ko.computed(function(){
            var full_address = self.house_number() +" "+ self.street_name();
            if (self.unit() != null || self.unit(), length > 0){
                full_address = full_address + " " + self.unit();
             }
            return full_address.trim();
        });
        self.zipcode = ko.observable("");
        self.city = ko.observable("");
        self.state = ko.observable("");
        self.full_address_ci_st_zip = ko.computed(function(){
            return  self.full_address() + " " + self.city() + " " +self.state()+ ", " + self.zipcode()
        });
        self.carts = ko.observableArray([]);
        self.latitude = ko.observable(null);
        self.longitude = ko.observable(null);
        self.geocode_status = ko.observable(null);
        self.valid = function(){
         return !(self.house_number.hasError())
                && !(self.street_name.hasError())
         };
        self.routes = ko.observableArray([]);

        if(data){

            self.id(data.info.properties.id);
            self.property_type(data.info.properties.property_type);
            self.house_number(data.info.properties.house_number);
            self.street_name(data.info.properties.street_name);
            self.unit(data.info.properties.unit);
            self.zipcode(data.info.properties.zipcode);
            self.city(data.info.properties.city);
            self.state(data.info.properties.state);
            self.carts(data.info.properties.carts);
            self.latitude(null);
            self.longitude(null);
            var routes = $.map(data.info.routes, function(item){
                return new cartlogic.Route(item)
            });

            self.routes(routes);
        }

    }

    cartlogic.Location = Location;

})(window.cartlogic);

/**
 *
 * User: jbennett
 * Date: 3/5/13
 * Time: 10:57 AM
 *
 */




(function (cartlogic) {

    function LocationSearchViewModel() {

        self.this;

        self.address = ko.observable("");
        self.selected_address = ko.observable("");
        self.addresses = ko.observableArray([]);

        self.searchAddress = function () {
            console.log(self.address().length);
            if (self.address().length == 5) {
                console.log("in the search");

                data = {"address":self.address()};

                $.getJSON(location_api_search, data, function (data) {
                    var addressList = $.map(data.results, function (item) {
                        return new cartlogic.Location(item);
                    });

                    self.addresses(addressList);

                });

            }
        };


    }

    cartlogic.LocationSearchViewModel = LocationSearchViewModel;


})(window.cartlogic);

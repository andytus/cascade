/**
 *
 * User: jbennett
 * Date: 3/5/13
 * Time: 10:57 AM
 *
 */




(function (cartlogic) {

    function LocationSearchViewModel() {

        var self = this;

        console.log("in location search");


        self.input_address = ko.observable("");
        self.selected_address = ko.observable("");
        self.addresses = ko.observableArray([]);
        self.server_message = ko.observable("");


        self.search = function () {
            console.log(self.input_address());

            if (self.input_address().length == 5) {


                data = {"address":self.input_address()};

                $.getJSON(location_api_search, data, function (data) {
                    var addressList = $.map(data, function (item) {
                        return new cartlogic.Location(item);
                    });

                    self.addresses(addressList);

                    //checking address lengths and adding the appropriate message
                    if (addressList.length == 0) {
                        self.server_message('<span class="text-error"> No Address Found! </span><br>' +
                            '<i class="text-info"> To add new, close this window and click on Customer >> New');
                    } else if (addressList.length == 1) {
                       self.server_message('<span class="text-success">' +
                            'Found one, please select and Click next' + '</span>');
                    } else {
                        self.server_message('<span class="text-success">' + '<b>Found ' +
                            addressList.length + '</b>... please select one and Click next' + '</span>');
                    }

                });


            }
        }
    }


    cartlogic.LocationSearchViewModel = LocationSearchViewModel;


})(window.cartlogic);

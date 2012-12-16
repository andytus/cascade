/**
 *
 * User: joe.bennett
 * Date: 12/10/12
 * Time: 3:12 PM
 * Uses Knockout js to get carts from server
 *
 */

function Cart(data){
    this.cart_serial = ko.observable((data.cart.serial) || "It's Missing");
    this.cart_id = ko.observable((data.cart.id));
    this.cart_url = ko.observable((cart_url + data.cart.id));
    this.cart_type = ko.observable((data.cart.cart_type) || "?");
    this.cart_size = ko.observable((data.cart.size) || "?");
    this.customer_id = ko.observable((data.customer.id) || "");
    this.customer_name = ko.observable((data.customer.name) || "Unknown or Not Assigned");
    this.customer_url = ko.observable((customer_url || "") + this.customer_id);

    this.address = ko.observable(data.location.properties.house_number + " " + data.location.properties.street_name);
    if (data.location.properties.unit){
        this.address(this.address()+ " " + "Unit: " + data.location.properties.unit);
    }
    this.latitude = ko.observable((data.location.geometry.coordinates[1]) || 0);
    this.longitude = ko.observable((data.location.geometry.coordinates[0]) || 0);
}

function CartSearch(type, value){
    this.type = type;
    this.value = value;
}

function CartListViewModel(){
    var self = this;
    //Incoming from server (search_parameters, page, count, etc..)
    self.search_for_type = ko.observable("");
    self.search_for_value = ko.observable("");
    self.carts = ko.observableArray([]);
    self.count = ko.observable("");
    self.page = ko.observable(1);

    //Outgoing to the server
    self.search_type = ko.observable("address");
    self.search_value = ko.observable();
    self.search_placeholder = ko.observable("Cart Search");
    self.search_query = ko.computed(function(){
    // Create a search object from the search_type and search_value
        search = new CartSearch(self.search_type, self.search_value);
        return ko.toJSON(search);
    });
    self.getSearchInfo = function(data, event){
        // Getting the search type for the clicked on drop down
        self.search_type(event.target.id);
        // Just clearing the value of the search input and changing the placeholder of the text to help the user.
        self.search_placeholder(event.target.title);
    };
    self.getData = function(params, page){
        //#TODO send in a dictionary of values for parameters. Construct in another function ...get existing params values(if linking to page) or set base on search
        // The search_parameters data comes from the source request
        // (placed as a template variable at the top of the cart_search.html).
        var url = "/cascadecart/api/cart/search/?format=jsonp&callback=?";
        self.search_for_type(params.type);
        self.search_for_value(params.value);


        // Remove active class from all pages and add to current page id (i.e. number)
        $(".page").removeClass("active");
        $("#"+ page).addClass("active");

        if (typeof page !== "undefined"){
            //get the page number if not undefined and add to the url (i.e. going to next page)
            //add through click event to a knockoutjs template the page links.

            self.page(page);
            url = url + "&page="+ page;

        }

        $.getJSON(url,
         params,
        //function creates and array of carts based on return from the server
        function (data) {
            self.count(data.count);
            var mappedCarts = $.map(data.results, function(item){
                return new Cart(item);
                });
            self.carts(mappedCarts);
            //self.count(data.count);
        } );
    };
    // sort of a default call of the fist page onload
    self.getData(search_parameters, 1);
}

$(document).ready(function () {
     ko.applyBindings(new CartListViewModel());
});

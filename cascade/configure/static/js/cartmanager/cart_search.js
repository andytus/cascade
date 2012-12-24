/**
 *
 * User: joe.bennett
 * Date: 12/10/12
 * Time: 3:12 PM
 * Uses Knockout js to get carts from server
 *
 */



function Cart(data) {
    /** Creates a Cart object returns to the view array **/
    this.cart_serial = ko.observable((data.cart.serial) || "It's Missing");
    this.born_date = ko.observable(new Date(data.cart.born_date).toDateString());
    this.current_status = ko.observable(data.cart.current_status);
    this.cart_id = ko.observable((data.cart.id));
    this.cart_url = ko.observable((cart_url + data.cart.serial));
    this.cart_type = ko.observable((data.cart.cart_type) || "?");
    this.cart_size = ko.observable((data.cart.size) || "?");
    this.customer_id = ko.observable((data.customer.id) || "");
    this.customer_name = ko.observable((data.customer.name) || "Unknown or Not Assigned");
    this.customer_url = ko.observable((customer_url || "") + this.customer_id);

    this.address = ko.observable(data.location.properties.house_number + " " + data.location.properties.street_name);
    if (data.location.properties.unit) {
        this.address(this.address() + " " + "Unit: " + data.location.properties.unit);
    }
    this.latitude = ko.observable((data.location.geometry.coordinates[1]) || 0);
    this.longitude = ko.observable((data.location.geometry.coordinates[0]) || 0);
}
function CartListViewModel() {
    /**  **/
    var self = this;
    //Incoming from server (search_parameters, page, count, etc..)
    self.search_for_type = ko.observable("");
    self.search_for_value = ko.observable("");
    self.carts = ko.observableArray([]);
    self.count = ko.observable(0);
    self.page = ko.observable(1);
    //#TODO Implement records per page (hard coded in html for now)
    self.records_per_page = ko.observable(30);
    self.total_pages = ko.computed(function () {
        return (Math.round(self.count() / self.records_per_page()));
    });

    //methods or functions on this model class

    self.Decorator = function () {
        $('.cart-info-serial').popover({
            trigger:'hover',
            placement:'bottom',
            title:'Cart Serial',
            html:true,
            content:function () {
                return '<h3>' + $(this).text() + '</h3>'
            }
        });
    };

    self.getData = function (params, page) {
        //#TODO send in a dictionary of values for parameters. Construct in another function ...get existing params values(if linking to page) or set base on search
        // The search_parameters data comes from the source request
        // (placed as a template variable at the top of the cart_search.html).


        var url = "/cascadecart/api/cart/search/?format=jsonp&callback=?";
        self.search_for_type(params.type);
        self.search_for_value(params.value);

        // Remove active class from all pages and add to current page id (i.e. number)
        $(".page").removeClass("active");
        $("#" + page).addClass("active");
        $(document).scrollTop($("#top").offset().top);


        if (typeof page !== "undefined") {
            //get the page number if not undefined and add to the url (i.e. going to next page)
            //add through click event to  a knockoutjs template the page links.

            self.page(page);
            url = url + "&page=" + page;
        }

        $.getJSON(url,
            params,
            //function creates and array of carts based on return from the server
            function (data) {
                if (data.count == 1) {
                    window.location.replace(cart_url + data.results[0].cart.serial)
                }
                var mappedCarts = $.map(data.results, function (item) {
                    return new Cart(item);
                });
                self.carts(mappedCarts);
                self.count(data.count);
            });

    };
    // sort of a default call of the fist page onload
    self.getData(search_parameters, 1);

}

$(document).ready(function () {

    ko.applyBindings(new CartListViewModel(), document.getElementById("results"));

});

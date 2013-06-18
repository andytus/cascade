/**
 *
 * User: jbennett
 * Date: 2/27/13
 * Time: 4:03 PM
 *
 */


//View Model for Cart Searches

(function (cartlogic){



    function CartsListViewModel(){

    /**  **/
    var self = this;
    //Incoming from server (search_parameters, page, count, etc..)
    self.search_for_type = ko.observable("");
    self.search_for_value = ko.observable("");
    self.carts = ko.observableArray([]);
    self.count = ko.observable(0);
    self.page = ko.observable(1);
    //#TODO Implement records per page (hard coded in html for now)
    self.records_per_page = ko.observable(35);
    self.total_pages = ko.computed(function () {
        return (Math.round(self.count() / self.records_per_page()));
    });

    //methods or functions on this model class

    self.Decorator = function () {
        $('.cart-info-link').popover({
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

       // var url = cart_search_api + "?format=jsonp&callback=?";
        var url = cart_search_api;


        // Remove active class from all pages and add to current page id (i.e. number)
        $(".page").removeClass("active");
        $("#" + page).addClass("active");
        $(document).scrollTop($("#top").offset().top);



        if (typeof page !== "undefined") {
            //get the page number if not undefined and add to the url (i.e. going to next page)
            //add through click event to  a knockoutjs template the page links.

           self.page(page);
          //  url = url + "&page=" + page;
           params.page = page;

        }


        $.ajax({

            url: url,
            data: params,
            dataType: 'json', contentType:"application/json",
            success: function (data) {
                if (data.count == 1) {
                    //if you get an exact match just forward to the carts profile page
                    window.location.replace(cart_url + data.results[0].cart.serial)
                }
                var mappedCarts = $.map(data.results, function (item) {
                    return new cartlogic.Cart(item);
                });

                self.carts(mappedCarts);
                self.count(data.count);
                //just fill in the search type and search value for header
                self.search_for_type(params.type);
                self.search_for_value(params.value);

                //hide message and show results header
                $("#message").hide();
                $("#result-header").show();
            },

            error: function(data){
                $("#message").removeClass("alert-info").addClass("alert-error").html("Error:" + data.statusText)
            }

        });

    };
    // sort of a default call of the fist page onload
    self.getData(search_parameters, 1);

}
    //add cartListView to cartlogic namespace
    cartlogic.CartsListViewModel = CartsListViewModel;

}(window.cartlogic));

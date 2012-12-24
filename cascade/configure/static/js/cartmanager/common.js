/**
 *
 * User: joe.bennett
 * Date: 12/21/2012
 * Time: 2:10 PM
 *
 *
 */

function CartSearch(type, value){
    this.type = type;
    this.value = value;
}

function CartSearchViewModel() {
    var self = this;
    //Outgoing to the server
    self.search_type = ko.observable("address");
    self.search_value = ko.observable();
    self.search_placeholder = ko.observable("Cart Search");
    self.search_query = ko.computed(function(){

     return ko.toJSON(new CartSearch(self.search_type, self.search_value));
    });

    self.getSearchInfo = function(data, event){
        // Getting the search type from the clicked on drop down
        self.search_type(event.target.id);
        // Just clearing the value of the search input and changing the placeholder of the text to help the user.
        self.search_placeholder(event.target.title);
    };
}

$(document).ready(function () {
    ko.applyBindings(new CartSearchViewModel(), document.getElementById("cart_search_form"));

});

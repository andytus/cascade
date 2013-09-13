/**
 *
 * User: jbennett
 * Date: 2/27/13
 * Time: 10:57 AM
 * Summary:
 * This model is intended to be used for look up only (i.e. listing) and does not provide
 * full set of attributes for carts
 */

(function (cartlogic){

function Cart(data){
     var self = this;
    /** Creates a Cart object returns to the view array **/
    self.cart_serial = ko.observable((data.cart.serial) || "It's Missing");
    self.born_date = ko.observable(new cartlogic.DateFormat(data.cart.born_date).full_date);
    self.current_status = ko.observable(data.cart.current_status);
    self.cart_id = ko.observable((data.cart.id));
    self.cart_url = ko.observable((cart_url + data.cart.serial));
    self.cart_type = ko.observable((data.cart.cart_type));
    self.cart_size = ko.observable((data.cart.size) || "?");
    self.customer_id = ko.observable((data.customer.id) || "");
    self.customer_name = ko.observable((data.customer.name) || "Unknown or Not Assigned");
    self.customer_url = ko.observable((customer_url || "") + this.customer_id());
    self.current_status_level = ko.observable(data.cart.current_status_level);
    if(data.location){
    self.address = ko.observable(data.location.properties.house_number + " " + data.location.properties.street_name);
    if (data.location.properties.unit) {
        this.address(this.address() + " " + "Unit: " + data.location.properties.unit);
    }
    self.latitude = ko.observable((data.location.geometry.coordinates[1]) || 0);
    self.longitude = ko.observable((data.location.geometry.coordinates[0]) || 0);

    } else{

        self.address = ko.observable(data.inventory_location.properties.house_number + " " + data.inventory_location.properties.street_name);
        if (data.inventory_location.properties.unit) {
            this.address(this.address() + " " + "Unit: " + data.inventory_location.properties.unit);
        }
        self.latitude = ko.observable((data.inventory_location.geometry.coordinates[1]) || 0);
        self.longitude = ko.observable((data.inventory_location.geometry.coordinates[0]) || 0);
     }
}

//add to cartlogic name space
cartlogic.Cart = Cart;

}(window.cartlogic));

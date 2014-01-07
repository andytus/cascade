/**
 *
 * User: jbennett
 * Date: 2/27/13
 * Time: 10:57 AM
 * Summary:
 * This model is intended to be used for look up only (i.e. listing) and does not provide
 * full set of attributes for carts
 */

(function (cartlogic) {

    function Cart(data) {
        var self = this;
        /** Creates a Cart object returns to the view array **/
       if(data.cart){
           self.cart_serial = data.cart.serial || "It's Missing";
           if (data.cart.born_date != null){
                self.born_date = new cartlogic.DateFormat(data.cart.born_date).full_date;

           }else{
               self.born_date = 'unknown'
           }

           self.current_status = data.cart.current_status__label;
           self.current_status__level = data.cart.current_status__level;

           self.cart_url = cart_url + data.cart.serial;
           self.cart_type__name = data.cart.cart_type__name || "?";
           self.cart_type__size = data.cart.cart_type__size || "?";
           self.cart_id =data.cart.id;
           self.cart_image = "cart_image"

       }else{
           self.cart_serial = "No Carts";
           self.born_date = ""
           self.cart_type__name = "";
           self.cart_type__size = "";
           self.current_status__level = ""
           self.current_status = ""
           self.cart_id = null
           self.cart_image = "cart_image_ghost"
       }
        //Checking for customer information
        if (data.customer){
        self.customer_id = data.customer.id || "";
        self.customer_name = data.customer.name;
        self.customer_url = customer_url + self.customer_id;
        } else{
        self.customer_id = "";
        self.customer_name = "Not Assigned";
        self.customer_url = "";
        }



        //Checking for location information
        if (data.location) {
            self.address = ko.observable(data.location.properties.house_number + " " + data.location.properties.street_name);
            if (data.location.properties.unit) {
                this.address(this.address() + " " + "Unit: " + data.location.properties.unit);
            }
            self.latitude = ko.observable((data.location.geometry.coordinates[1]) || 0);
            self.longitude = ko.observable((data.location.geometry.coordinates[0]) || 0);

        } else {

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

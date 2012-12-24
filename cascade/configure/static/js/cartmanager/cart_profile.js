/**
 * Created with PyCharm.
 * User: joe.bennett
 * Date: 12/22/12
 * Time: 12:16 AM
 * To change this template use File | Settings | File Templates.
 */
//last_latitude: "0",
//    last_longitude: "0",
//    rfid: "121016134330111111111111",
//    serial_number: "1111112",
//    size: 96,
//    current_status: "test",
//    cart_type: "Recycle",
//    last_updated: "2012-12-08T15:33:03.147Z",
//    born_date: "2012-10-07T04:00:00Z"

//
//"customer": null,
//    "id": 1,
//    "house_number": "2",
//    "street_name": "Cascade",
//    "unit": null,
//    "city": "DEFAULT",
//    "state": "NA",
//    "zipcode": 12345,
//    "latitude": null,
//    "longitude": null,
//    "route": null,
//    "type": "Inventory"

function Location(data){
    this.id = ko.observable(data.id);
    this.house_number = ko.observable(data.house_number);
    console.log(data.street_name);
    this.street_name = ko.observable(data.street_name);
}


function CartProfileViewModel() {

    var self = this;

    self.last_longitude = ko.observable();
    self.last_latitude = ko.observable();
    self.rfid = ko.observable();
    self.serial_number = ko.observable(serial_number);
    self.size = ko.observable();
    self.cart_type = ko.observable();
    self.current_status = ko.observable();
    self.last_updated = ko.observable();
    self.born_date = ko.observable();
    //location information
    self.location_house_number = ko.observable();
    self.location_street_name = ko.observable();
    self.location_unit = ko.observable();
    self.location_address = ko.computed(function(){
        address = self.location_house_number() + " " + self.location_street_name();
        if (self.location_unit()){
            address = address + self.location_unit();
        }
        return address});
    self.location_latitude = ko.observable();
    self.location_longitude = ko.observable();
    self.location_type = ko.observable();

    //customer information
    self.customer_name = ko.observable();



    self.getCartData = function () {
        $.getJSON(cart_url + serial_number, function (data) {
            console.log(data);
            self.rfid(data.rfid);
            self.size(data.size);
            self.cart_type(data.cart_type);
            self.current_status(data.current_status);
            self.last_updated(new Date(data.last_updated).toDateString());
            self.born_date(new Date(data.born_date).toDateString());

            //location information
            self.location_house_number(data.location.house_number);
            self.location_street_name(data.location.street_name);
            self.location_unit(data.location.unit);
            self.location_latitude(data.location.latitude);
            self.location_longitude(data.location.longitude);
            self.location_type(data.location.type);
            self.customer_name(data.location.customer.info.name);

        })
    };

    self.saveCartData = function (){

    };

    self.getLocation = function (){

    };

    self.updateLocation = function (){

    };

    self.getCartData()
}


$(document).ready(function(){
    ko.applyBindings(new CartProfileViewModel(), document.getElementById("cart_profile"))
    }
);


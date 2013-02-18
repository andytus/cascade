/**
 * User: joe.bennett
 * Date: 12/22/12
 * Time: 12:16 AM
 * s.
 */



function Location(data) {
    this.id = ko.observable(data.id);
    this.house_number = ko.observable(data.house_number);
    this.street_name = ko.observable(data.street_name);
}

function StatusOption(data) {
    this.id = ko.observable(data.id);
    this.level = ko.observable(data.level);
    this.label = ko.observable(data.label);
}

function TypeOption(data) {
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
    this.size = ko.observable(data.size);
    this.site = ko.observable(data.site);
}


function CartProfileViewModel() {

    var self = this;

    self.last_longitude = ko.observable();
    self.last_latitude = ko.observable();
    self.rfid = ko.observable("");
    self.serial_number = ko.observable(serial_number);

    self.id = ko.observable("");
    self.cart_profile_url = ko.computed(function () {
        return cart_app_url + serial_number
    });
    self.size = ko.observable("");
    self.cart_type = ko.observable("");
    self.cart_type_id = ko.observable("");
    self.last_updated = ko.observable("");
    self.born_date = ko.observable("");
    //location information
    self.location_house_number = ko.observable("");
    self.location_street_name = ko.observable("");
    self.location_unit = ko.observable("");
    self.location_address = ko.computed(function () {
        address = self.location_house_number() + " " + self.location_street_name();
        if (self.location_unit()) {
            address = address + " Unit: " + self.location_unit();
        }
        return address
    });
    self.location_latitude = ko.observable();
    self.location_longitude = ko.observable();
    self.location_type = ko.observable();

    //customer information
    self.customer_id = ko.observable();
    self.customer_name = ko.observable();
    self.customer_url = ko.computed(function () {
        return customer_app_url + self.customer_id()
    });


    //status information
    self.current_status_id = ko.observable();
    self.current_status = ko.observable();
    self.current_status_level = ko.observable();
    self.cart_status_options = ko.observableArray([]);
    self.changeCartStatus = ko.computed(function () {
        //#TODO Got to be a cleaner way
        $('#cart-info-edit-status').change(function () {
            var status = $("#cart-info-edit-status option:selected");
            self.current_status(status.text());
            level = self.cart_status_options();
            var match = ko.utils.arrayFirst(self.cart_status_options(), function (item) {
                return status.val() == item.id();
            });

            self.current_status_level(match.level())

        });

        //type information
        self.cart_type_options = ko.observableArray([]);
        self.changeCartType = ko.computed(function () {
            $('#cart-info-edit-type').change(function () {
                var type = $('#cart-info-edit-type option:selected').text();
                self.cart_type(type);
            })
        });

    });


    self.getCartData = function () {
        $.getJSON(cart_api_url + serial_number, function (data) {

            cart_id = data.id;
            self.id(data.id);
            self.rfid(data.rfid);
            self.size(data.cart_type.size);
            self.cart_type(data.cart_type.name);
            self.cart_type_id(data.cart_type.id);
            self.last_updated(new Date(data.last_updated).toDateString());
            self.born_date(new Date(data.born_date).toDateString());

            //location information
            self.location_house_number(data.location.house_number);
            self.location_street_name(data.location.street_name);
            self.location_unit(data.location.unit);
            self.location_latitude(data.location.latitude);
            self.location_longitude(data.location.longitude);
            self.location_type(data.location.type);

            //customer information
            self.customer_name(data.location.customer.info.name);
            self.customer_id(data.location.customer.info.id);

            //status information
            self.current_status_id(data.current_status.id);
            self.current_status_level(data.current_status.level);
            self.current_status(data.current_status.label);

            //Calling to get cart type options for this cart
            //filters based on size and needs to get the size from the current cart size
            self.getTypeOptions();
            //Calling to get the cart status options
            self.getStatusOptions();
            self.map();

        })
    };
    self.getStatusOptions = function () {
        $.getJSON(cart_status_options_api_url + "?format=jsonp&callback=?", function (data) {
            var cartStatusOptions = $.map(data, function (item) {
                return new StatusOption(item);
            });
            self.cart_status_options(cartStatusOptions);
            //set drop down to current status
            $("#cart-info-edit-status option[value='" + self.current_status_id() + "']").attr("selected", "selected");
        })
    };

    self.getTypeOptions = function () {
        url = cart_type_options_api_url + "?format=jsonp&callback=?";
        data = {'size':self.size()};
        $.getJSON(url, data, function (data) {
            var cartTypeOptions = $.map(data, function (item) {
                return new TypeOption(item)
            });
            self.cart_type_options(cartTypeOptions);
            //Set drop down to current cart type
            $("#cart-info-edit-type option[value='" + self.cart_type_id() + "']").attr("selected", "selected");
        })
    };

    self.saveCartData = function () {
        $.ajax(cart_api_url + serial_number, {
            data:ko.toJSON({current_status:self.current_status, cart_type:document.getElementById('cart-info-edit-type').value}),
            type:"post", contentType:"application/json",
            dataType:"jsonp",
            success:function (result) {
                console.log(result.time);
                self.last_updated(new Date(result.time).toDateString());
                $("#message").addClass("alert-success").show();
                $("#message-type").text("Success! ");
                $("#message-text").text(result.message);
                $('.close').click(function () {
                    $('#message').hide();
                 //Call get cart to refresh the cart model
                 self.getCartData()
                })

            },
            error:function (result) {
                console.log(result)
            }
        })


    };

    self.map = function(){

       var cartLatlng = new google.maps.LatLng(self.location_longitude(), self.location_latitude());
       var mapOptions = {
            center: cartLatlng,
            zoom: 12,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        var map = new google.maps.Map(document.getElementById("map_canvas"),
            mapOptions);

        var image = new google.maps.MarkerImage(
            static_url + 'img/marker-images/image.png',
            new google.maps.Size(40,50),
            new google.maps.Point(0,0),
            new google.maps.Point(20,50)
        );

        var shadow = new google.maps.MarkerImage(
            static_url +'img/marker-images/shadow.png',
            new google.maps.Size(68,50),
            new google.maps.Point(0,0),
            new google.maps.Point(20,50)
        );

        var shape = {
            coord: [35,4,36,5,37,6,37,7,36,8,35,9,35,10,35,11,35,12,35,13,35,14,35,15,35,16,35,17,34,18,34,19,34,20,34,21,34,22,34,23,34,24,34,25,34,26,34,27,33,28,33,29,33,30,33,31,33,32,33,33,33,34,33,35,33,36,33,37,33,38,33,39,33,40,33,41,33,42,33,43,29,44,28,45,27,46,27,47,19,47,16,46,13,45,8,44,7,43,6,42,5,41,5,40,5,39,5,38,5,37,6,36,8,35,10,34,10,33,10,32,9,31,9,30,9,29,9,28,9,27,9,26,9,25,9,24,9,23,9,22,8,21,8,20,7,19,5,18,5,17,5,16,5,15,5,14,4,13,4,12,4,11,4,10,3,9,3,8,3,7,2,6,6,5,15,4,35,4],
            type: 'poly'
        };

        var marker = new google.maps.Marker({
            draggable: true,
            raiseOnDrag: true,
            icon: image,
            shadow: shadow,
            shape: shape,
            position: cartLatlng,
            map: map,
            title: self.rfid()
        });

        google.maps.event.addListener(marker, 'dragend', function() {
            console.log(marker.getPosition());
        });


    };



    self.getLocation = function () {

    };

    self.updateLocation = function () {

    };

//call the api to get the data on load
    self.getCartData();

}

function Tickets(data) {
    this.status = ko.observable(data.status);
    this.service_type = ko.observable(data.service_type);
    this.success_attempts = ko.observable(data.success_attempts);
    this.date_created = (new Date(data.date_created).toDateString());
    this.date_last_accessed = ko.observable(new Date(data.date_last_accessed).toDateString());
    this.house_number = ko.observable(data.house_number);
    this.street_name = ko.observable(data.street_name);
    this.unit = ko.observable(data.unit);
    this.removed_cart = ko.observable(data.removed_cart);
    this.delivered_cart = ko.observable(data.delivered_cart);
    this.audit_cart = ko.observable(data.audit_cart);
}

function TicketsModelView(records_per_page) {
    var self = this;
    self.count = ko.observable(0);
    self.page = ko.observable(1);
    //#TODO Implement records per page (hard coded in html for now)
    self.records_per_page = ko.observable(40);
    self.total_pages = ko.computed(function () {
        return (Math.round(self.count() / self.records_per_page()));

    });
    self.sort_default = ko.observable('status__service_status');

    //cart tickets
    self.tickets = ko.observableArray();

    self.ticket_table_headers = ko.observableArray(
        //#TODO ugly but works
        [
            {field:'status__service_status', displayName:'Status', sort:ko.observable(0)},
            {field:'service_type__code', displayName:'Type', sort:ko.observable(0)},
            {field:'success_attempts', displayName:'Attempts', sort:ko.observable(0)},
            {field:'date_created', displayName:'Created', sort:ko.observable(0)},
            {field:'date_last_accessed', displayName:'Updated', sort:ko.observable(0)},
            {field:'location__house_number', displayName:'House', sort:ko.observable(0)},
            {field:'location__street_name', displayName:'Street', sort:ko.observable(0)},
            {field:'location__unit', displayName:'Unit', sort:ko.observable(0)},
            {field:'cart_rfid', displayName:'Cart RFID', sort:ko.observable(0)}
        ]
    );


    self.getTickets = function (serial_number, page) {
        url = tickets_api_download;
        self.page(page); //update page
        data = {"serial_number":serial_number, "page":page, "sort_by":self.sort_default()};


        $.getJSON(url, data, function (data) {
            self.count(data.count);
            var cartTickets = $.map(data.results, function (item) {
                return new Tickets(item);
            });
            self.tickets(cartTickets);
        });
    };


    (function () {
        self.getTickets(serial_number, 1, 'status__service_status');

    })();

    self.sortTickets = function (serial_number, page, sort_by) {

        for (var i=0; i < self.ticket_table_headers().length; i++){
            if (self.ticket_table_headers()[i].field != sort_by.field)
            self.ticket_table_headers()[i].sort(0);
        }

       if (sort_by.sort() == 0) {
            sort_by.sort(1);
            self.sort_default(sort_by.field);
            self.getTickets(serial_number, 1);

        }

        else if (sort_by.sort() == 1) {
            sort_by.sort(2);
            //rest the current default to 0 sort
            console.log(sort_by.sort());
            self.sort_default("-" + sort_by.field);
            self.getTickets(serial_number, 1);
        }
        else {
           //rest the current default to 0 sort
            sort_by.sort(0);
           }


    }
}

$(document).ready(function () {
        ko.applyBindings(new CartProfileViewModel(), document.getElementById("cart_profile"));
        ko.applyBindings(new TicketsModelView(1), document.getElementById("ticket_panel"));


    }
);






(function (cartlogic) {

  function  CustomerNewViewModel(){

      var self = this;

      //creates a blank customer
      self.customer = ko.observable(new cartlogic.Customer);
      self.location = ko.observable(new cartlogic.Location);
      //location information
     // self.house_number = ko.observable();
     // self.street_name = ko.observable();

      //TODO call server to get unique street after length of say 4
      self.update_street = function(){

      };

      //returned from the Geocoder and sent on to mapping
      //TODO selects only the top result from the coder for now
      self.geocoded_results = ko.observableArray([]);

     // self.street_suffix = ko.observable();
      self.suffix_defaults = new cartlogic.streetSuffix().get_abbreviated();


     // self.unit = ko.observable(null);
     // self.zipcode = ko.observable();

     // self.latitude = ko.observable();

    //  self.longitude = ko.observable()

    //  self.state = ko.observable();
    //  self.city = ko.observable();
/*

      self.full_address = ko.computed( function(){
          var address = self.house_number() + " " + self.street_name();
          if (self.unit()){
              address = address +" "+ self.unit()

          }

          address = address +" "+ self.street_suffix() +  " " + self.city() + ", " + self.state() + " " + self.zipcode();
          return address;
      });
*/



      //state and city, can use a default
      self.use_default_state_city = ko.observable(true);

      self.default_zipcodes = ko.observableArray([]);

      self.map_style =  new cartlogic.MapStyle();


      self.geocoder_type = ko.observable('google');


      self.mapIt = function(){
          var map_verify = new cartlogic.FormStep(3, "Map Verify", "MapLocation", {message:"Verify Location"});
          console.log(self.stepModels().length);

          //Only add this step if its not been added
          if (self.stepModels().length <= 4){
                self.stepModels.splice(2, 0, map_verify);
          }
          self.currentStep(self.stepModels()[2]);
          //just give the map a little time to load:
          var address_map = new cartlogic.GeocodeMap(document.getElementById('map_canvas_address'), 'address_lat','address_lon', 'geocode_status', {coder:  self.geocoder_type(), address: self.location().full_address_ci_st_zip()});
          //do the mapping:
          address_map.geocode();
        };



      self.stepModels = ko.observableArray([

      //    new cartlogic.FormStep(1, "Title", "id",
      //        {services:object, message:"Message" }),

          new cartlogic.FormStep(1, "Add Customer Information", "CustomerInfo",
              {message:"Create New Customer Wizard" }),

          new cartlogic.FormStep(2, "Add Address Information", "AddressInfo", {message: "Add Address"}),

          new cartlogic.FormStep(4, "Confirm Save", "ConfirmSave", {message: "Confirm Save"}),

          new cartlogic.FormStep(5, "Complete", "Complete", {message: "Verify Location"})

      ]);

      self.get_default_info = function(){
          url = admin_api_location + "?format=jsonp&callback=?";

          $.getJSON(url, function (data) {
              self.location().state(data.info.state);
              self.location().city(data.info.city);
              var zipcodes = $.map(data.info.zipcodes, function(item){
                return item.zipcode;

              });
              self.default_zipcodes(zipcodes);
              //adding blank at the beginning
              self.default_zipcodes.unshift('Select One');

             //$("#cart-info-edit-status option[value='" + self.cart().current_status_id() + "']").attr("selected", "selected");
          });

      };

      //Wizard Step Navigation

      self.currentStep = ko.observable(self.stepModels()[0]);

      self.currentIndex = ko.computed(function () {

          return self.stepModels.indexOf(self.currentStep());
      });

      self.isConfirmStep = ko.computed(function () {
          return self.currentIndex() == self.stepModels().length - 2;

      });


      self.isCompleteStep = ko.computed(function(){
          return self.currentIndex() == self.stepModels().length -1;
      });

      self.canGoNext = ko.computed(function () {
          return self.currentIndex() < self.stepModels().length - 1;
      });


      self.goNext = function () {
          if (self.canGoNext()) {
              self.currentStep(self.stepModels()[self.currentIndex() + 1]);
          }
      };

      self.canGoPrevious = ko.computed(function () {
          //can go to previous if the index is greater than zero and less than the last step (i.e. success)
          return self.currentIndex() > 0 && self.currentIndex() < self.stepModels().length -1;
      });

      self.goPrevious = function () {
          if (self.canGoPrevious()) {
              self.currentStep(self.stepModels()[self.currentIndex() - 1]);
          }
      };

     self.get_default_info();

   }

    cartlogic.CustomerNewViewModel = CustomerNewViewModel


})(window.cartlogic);



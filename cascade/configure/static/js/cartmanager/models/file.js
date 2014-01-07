/**
 *
 * User: jbennett
 * Date: 6/13/13
 * Time: 1:22 PM
 *
 */
(function (cartlogic){

    function File(data){

    var self = this;
    self.id = ko.observable(data.id);
    self.status = ko.observable(data.status);
    self.size = ko.observable(parseFloat(data.size/1024).toFixed(2));
    self.uploaded_by = ko.observable(data.uploaded_by);
    self.date_uploaded = ko.observable(new cartlogic.DateFormat(data.date_uploaded).full_date_time);
    self.file_path =  ko.observable(data.file_path);
    self.num_records = ko.observable(data.num_records);
    self.num_good = ko.observable(data.num_good);
    self.num_error = ko.observable(data.num_error);
    self.file_kind = ko.observable(data.file_kind);
    }

//add to cartlogic name space
    cartlogic.File = File;

}(window.cartlogic));
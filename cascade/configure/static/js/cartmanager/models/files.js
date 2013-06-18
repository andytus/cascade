/**
 *
 * User: jbennett
 * Date: 6/13/13
 * Time: 1:22 PM
 *
 */
(function (cartlogic){

    function File(data, type){

    var self = this;
    self.status = data.status;
    self.uploaded_by = data.uploaded_by;
    self.date_uploaded = new Date(data.date_uploaded).toDateString();
    self.file_path =  data.file_path;
    self.records_processed = data.records_processed;


    }

//add to cartlogic name space
    cartlogic.File = File ;

}(window.cartlogic));
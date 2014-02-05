/**
 *
 * User: jbennett
 * Date: 2/4/14
 * Time: 10:09 AM
 *
 */



(function (cartlogic){

   function ReportFile(data){

       this.id = data.id;
       this.file = data.file;
       this.report__id = data.report__id;
       this.report__name = data.report__name;
       this.last_generated = ko.observable(new cartlogic.DateFormat(data.last_generated).full_date_time);
       this.description = data.description;
       this.update_in_progress = ko.observable(data.update_in_progress);
   }

//add to cartlogic name space
    cartlogic.ReportFile = ReportFile;

}(window.cartlogic));
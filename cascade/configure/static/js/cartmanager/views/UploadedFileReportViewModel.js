



(function (cartlogic){

    function UploadedFileReportViewModel(){
        var self = this;
        self.file_type = ko.observable(file_type);
        self.file_status_options = ko.observable(['ALL','PENDING', 'UPLOADED', 'FAILED'])
        self.file_status = ko.observable(file_status);
        self.file_id = ko.observable(file_id)
        self.count = ko.observable(0);
        self.page = ko.observable(1);
        //#TODO Implement records per page (hard coded in html for now)
        self.records_per_page = ko.observable(25);
        self.total_pages = ko.computed(function () {
            return (Math.round(self.count() / self.records_per_page()));
        });
        self.sort_default = ko.observable('date_uploaded');
        self.file_list = ko.observableArray([]);
        self.file_table_headers = ko.observableArray(
            [
                {field:'uploaded_by', displayName:'Uploaded By', sort:ko.observable(0)},
                {field:'size', displayName:'Size (MB)', sort:ko.observable(0)},
                {field:'date_uploaded', displayName:'Date Uploaded', sort:ko.observable(0)},
                {field:'status', displayName:'Status', sort:ko.observable(0)},
                {field:'num_records', displayName:'Total Records', sort:ko.observable(0)},
                {field:'num_good', displayName:'Good', sort:ko.observable(0)},
                {field:'num_error', displayName:'Error', sort:ko.observable(0)},
                {field:'file_kind', displayName:'File Type', sort:ko.observable(0)},
             ]
        );


        self.getUploadedFiles = function(page, sort_by, format, file_id) {
           var data = {sort_by:self.sort_default()};
           self.page(page);


          if (typeof sort_by != 'undefined' && sort_by != null) {

               for (var i = 0; i < self.file_table_headers().length; i++) {
                    if (self.file_table_headers()[i].field != sort_by.field)
                        self.file_table_headers()[i].sort(0);
                }

                if (sort_by.sort() == 0) {
                    sort_by.sort(1);
                    self.sort_default(sort_by.field);

                }

                else if (sort_by.sort() == 1) {
                    sort_by.sort(2);
                    self.sort_default("-" + sort_by.field);

                }
                else {
                    //reset the current default to 0 sort
                    sort_by.sort(0);
                }

            }

            if (self.file_type() != null){
                data.file_type = self.file_type();
            }
            if (self.file_status() != null){
                data.file_status = self.file_status();
            }

            if (file_id != 0 && self.file_id() != null){
              data.file_id = self.file_id();
            }

           $.ajax({
               url: upload_file_list_api_url,
               data: data,
               dataType:"jsonp",
               success: function(data){
                   self.count(data.count)
                   var files = $.map(data.results, function(item){
                       return new cartlogic.File(item)
                   });
                   self.file_list(files);


               },
               error: function(jqXHR){
                   $("#message").addClass("alert-error").show();
                        $("#message-type").text("Error!");
                        $("#message-text").text(jqXHR.statusText);
                        $('.close').click(function () {
                        $('#message').hide();
                        });
               }
            });
        };

     self.getUploadedFiles();

    }

cartlogic.UploadedFileReportViewModel = UploadedFileReportViewModel;

})(window.cartlogic);
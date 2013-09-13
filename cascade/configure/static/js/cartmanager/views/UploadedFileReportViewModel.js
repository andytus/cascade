(function (cartlogic) {

    function UploadedFileReportViewModel(file_type, file_status, file_id, upload_file_list_api_url) {

        var self = this;

        self.file_type = ko.observable(file_type);
        self.file_status_options = ko.observable(['ALL', 'PENDING', 'UPLOADED', 'FAILED']);
        self.file_status = ko.observable(file_status);
        self.file_id = ko.observable(file_id);
        self.file_list = ko.observableArray([]);
        self.sortOnServer = ko.observable(false);
        self.sortInfo = ko.observable();
        self.sort_by = ko.observable('status');

        self.pagingOptions = {
            pageSizes: ko.observableArray([100, 250, 500]),
            pageSize: ko.observable(100),
            totalServerItems: ko.observable(0),
            currentPage: ko.observable(1)
        };


        self.getPagedDataAsync = function () {
            var data = {};
            data.page = self.pagingOptions.currentPage();
            data.page_size = self.pagingOptions.pageSize();
            data.sort_by = self.sort_by();


            if (self.file_type() != null) {
                data.file_type = self.file_type();
            }
            if (self.file_status() != null) {
                data.file_status = self.file_status();
            }

            if (self.file_id() != 0 && self.file_id() != null) {
                data.file_id = self.file_id();
            }

            $.ajax({
                url: upload_file_list_api_url,
                data: data,
                dataType: "jsonp",
                success: function (data) {
                    self.pagingOptions.totalServerItems(data.count);
                    var files = $.map(data.results, function (item) {
                        return new cartlogic.File(item)
                    });
                    self.file_list(files);

                },
                error: function (jqXHR) {
                    $("#message").addClass("alert-error").show();
                    $("#message-type").text("Error!");
                    $("#message-text").text(jqXHR.statusText);
                    $('.close').click(function () {
                        $('#message').hide();
                    });
                }
            });
        }


        self.pagingOptions.currentPage.subscribe(function (page) {
            //setter for currentPage
            self.pagingOptions.currentPage(page);
            self.getPagedDataAsync();
        });

        self.pagingOptions.pageSize.subscribe(function (pageSize) {
            //setter for pageSize
            self.pagingOptions.pageSize(pageSize);
            self.getPagedDataAsync();

        });

        $('.run_query').click(function(){
                self.file_id(null);
                self.getPagedDataAsync();
         });


        self.sortInfo.subscribe(function (data) {
             //work around because koGrid bug calls sort twice:
            // See: http://stackoverflow.com/questions/15232644/kogrid-sorting-server-side-paging
            self.sortOnServer(!self.sortOnServer());
            if (!self.sortOnServer()) return;

            self.sort_by(self.sortInfo().column.field);
            if (self.sortInfo().direction == 'desc') {
                self.sort_by( "-" + self.sort_by());
            }
           self.getPagedDataAsync();

        });

       self.columns = [

            {field: 'id', displayName: 'id'},
            {field: 'status', displayName: 'Status'},
            {field: 'size', displayName: 'Size'},
            {field: 'uploaded_by', displayName: 'Uploaded By'},
            {field: 'date_uploaded', displayName: 'Uploaded On'},
            {field: 'num_records', displayName: 'Records'},
            {field: 'num_good', displayName: 'Good'},
            {field: 'num_error', displayName: 'Error'},
            {field: 'file_kind', displayName: 'File Type'}

        ]
        self.gridOptions = {
            data: self.file_list,
            enablePaging: true,
            useExternalSorting: true,
            pagingOptions: self.pagingOptions,
            sortInfo: self.sortInfo,
            columnDefs: self.columns,
            canSelectRows: false,
            footerRowHeight: 50,
            selectWithCheckboxOnly: true,
            showFilter: false
        }


    }

    cartlogic.UploadedFileReportViewModel = UploadedFileReportViewModel;

})(window.cartlogic);
/**
 *
 * User: jbennett
 * Date: 2/3/14
 * Time: 1:54 PM
 *
 */

( function (cartlogic) {

    function ReportFileListViewModel(report_type, report_list_api_url, report_generate_url) {
        var self = this;
        self.sort_by = ko.observable('report__name'); //TODO add default sort
        self.report_type = ko.observable(report_type);
        self.report_file_list = ko.observableArray([]);
        self.sortInfo = ko.observable();
        self.sortOnServer = ko.observable(false);
        self.selected_report = ko.observable();

        self.pagingOptions = {
            pageSizes: ko.observable([100, 250, 500]),
            pageSize: ko.observable(100),
            totalServerItems: ko.observable(0),
            currentPage: ko.observable(1)
        };


        self.getPagedDataAsync = function () {
            var data = {};
            data.page = self.pagingOptions.currentPage();
            data.page_size = self.pagingOptions.pageSize();
            data.sort_by = self.sort_by();

            if (self.report_type() != null) {
                console.log(report_type);
                data.report_type = self.report_type();
            }
            $.ajax({

                url: report_list_api_url + self.report_type(),
                dataType: "jsonp",
                success: function (data) {
                    self.pagingOptions.totalServerItems(data.count);
                    var report_files = $.map(data.results, function (item) {
                        return new cartlogic.ReportFile(item);
                    });

                    self.report_file_list(report_files);
                },

                error: function (jqXHR) {
                    $("#message").addClass("alter-error").show();
                    $("#message-type").text("Error!");
                    $("#message-text").text(jqXHR.statusText);
                    $(".close").click(function () {
                        $("#message").hide();
                    });
                }
            });

        }

        self.pagingOptions.currentPage.subscribe(function (page) {
            self.pagingOptions.currentPage(page);
            self.getPagedDataAsync();
        });


        self.sortInfo.subscribe(function (data) {

            //work around because koGrid bug calls sort twice:
            // See: http://stackoverflow.com/questions/15232644/kogrid-sorting-server-side-paging
            self.sortOnServer(!self.sortOnServer());
            if (!self.sortOnServer()) return;

            self.sort_by(self.sortInfo().column.field);
            if (self.sortInfo().direction == 'desc') {
                self.sort_by("-" + self.sort_by())
            }
            self.getPagedDataAsync();
        });


        self.getReportFileInfo = function (report_file_index, generate) {
            $.ajax({
                url: report_generate_url + self.report_file_list()[report_file_index].report__id,
                data: {'generate': generate},
                success: function (data) {
                  if (data.update_in_progress == 'No'){
                        self.getPagedDataAsync();
                        self.report_file_list()[report_file_index].update_in_progress('No');
                        self.report_file_list()[report_file_index].last_generated(
                            new cartlogic.DateFormat(data.last_generated));
                         $('#' + self.report_file_list()[report_file_index].id + "_refresh").toggleClass('active');
                    }

                },
                complete: function () {
                    if (self.report_file_list()[report_file_index].update_in_progress() == 'Yes') {
                        setTimeout(function(){self.getReportFileInfo(report_file_index, false)}, 5000)
                    } else {
                    $("#message-type").text("Success: ");
                    $("#message-text").text(self.report_file_list()[report_file_index].report__name +
                                            " report refresh complete.");
                    $('.close').click(function() {
                        $('#message').hide();
                    });
                   $("#message").removeClass("alert-error").addClass('alert-success').show();

                    }

                },
                error: function(data){
                    $("#message").removeClass("alert-info")
                        .addClass("alert-error")
                        .html("Error:" + data.statusText).show();
                }
            })
        }

        self.generateFile = function (data) {
            $('#' + data + "_refresh").toggleClass('active');
            var generate = true;
            var report_file_index = cartlogic.arrayFirstIndexOf(self.report_file_list(), function (item) {
                return data == item.id;
            });
            self.report_file_list()[report_file_index].update_in_progress('Yes');
            self.getReportFileInfo(report_file_index, generate)
        }


        //       <button class="btn-success has-spinner">
        //   <span class="spinner"><i class="icon-spin icon-refresh"></i></span>
        //   Foo
        // </button>

        self.report_download_cell_template = '<a style=\'margin-top: 2px;\' class=\'btn btn-small, btn-info\' ' +
            'data-bind="attr: {\'href\': $data.getProperty($parent)}"><i class=\'icon-download\'> </i>Save</a>';

        self.report_generate_report_cell_template = '<button style=\'margin-top: 2px;\' class=\' btn-small ' +
            'btn-success has-spinner\' data-bind=" attr:{\'id\': $data.getProperty($parent) + \'_refresh\' } , click: function(data, event) ' +
            '{$userViewModel.generateFile($data.getProperty($parent))}"><span class=\'spinner\'><i class=\'icon-spin icon-refresh\'> ' +
            '</i></span> Refresh</button>';

        self.columns = [

            {field: 'id', displayName: 'id', width: 100},
            {field: 'report__name', displayName: 'Report Name', width: '**'},
            {field: 'description', displayName: 'Description', width: '***'},
            {field: 'last_generated', displayName: 'Generated on', width: '*'},
            {field: 'file', displayName: 'Download', cellTemplate: self.report_download_cell_template, width: 100},
            {field: 'id', displayName: 'Generate', cellTemplate: self.report_generate_report_cell_template, width: 100}

        ]

        self.gridOptions = {
            data: self.report_file_list,
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

//add to cartlogic name space
    cartlogic.ReportFileListViewModel = ReportFileListViewModel;

}(window.cartlogic));
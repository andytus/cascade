/**
 *
 * User: Joe Bennett
 * Date: 9/10/13
 * Time: 3:26 PM
 * Takes a Date() object and converts
 * to d-m-yyyy
 */

(function (cartlogic){

    function DateFormat(string_date){
        var self = this;
        self.d = new Date(string_date);
        self.curr_date = self.d.getDate();
        self.curr_month = self.d.getMonth() + 1; //zero based
        self.curr_year = self.d.getFullYear();
        self.full_date =  self.curr_month + "-" + self.curr_date + "-" + self.curr_year;
        return self;
    };

    cartlogic.DateFormat = DateFormat;
}
)(window.cartlogic);
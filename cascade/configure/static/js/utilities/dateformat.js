/**
 *
 * User: Joe Bennett
 * Date: 9/10/13
 * Time: 3:26 PM
 * Takes a Date() object and converts
 * to d-m-yyyy
 */

(function (cartlogic) {

    function DateFormat(string_date) {
        var self = this;
        self.d = new Date(string_date);
        self.curr_date = self.d.getDate();
        self.curr_month = self.d.getMonth() + 1; //zero based
        self.curr_year = self.d.getFullYear();
        self.full_date = self.curr_month + "-" + self.curr_date + "-" + self.curr_year;
        self.am_pm = self.d.getHours() < 12 ? "am" : "pm";
        if (self.d.getHours() > 12){
        self.hours = self.d.getHours() - 12;
        }else if (self.d.getHours() == 0){
        self.hours = 12;
        } else{
        self.hours = self.d.getHours();
        }

        self.minutes = self.d.getMinutes();
        if (self.minutes < 10) {
            self.minutes = "0" + self.minutes;
        }
        self.time = self.hours + ":" + self.minutes + self.am_pm;
        self.full_date_time = self.full_date + " " + self.time;
        return self;
    };

    function TimeFormat(string_date) {
        var self = this;
        self.d = new Date(string_date);
        self.am_pm = self.d.getHours() < 12 ? "am" : "pm";
        self.hours = self.d.getHours() - 12;
        self.minutes = self.d.getMinutes();
        if (self.minutes < 10) {
            self.minutes = "0" + self.minutes;
        }
        self.time = self.hours + ":" + self.minutes + self.am_pm;
        return self;
    }


    cartlogic.TimeFormat = TimeFormat;
    cartlogic.DateFormat = DateFormat;
})(window.cartlogic);
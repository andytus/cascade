/**
 *
 * User: jbennett
 * Date: 4/3/13
 * Time: 11:51 AM
 *
 */


(function (utilities) {


    function validateKo() {


        ko.extenders.validate = function (target, options) {
            var self = this;
            self.filters = [
                {type:'email',
                    pattern:/(^$|^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$)/,
                    message:'Not a valid email address <br> (example: someone@someplace.com)'
                },
                {type:'phone',
                    pattern:/^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/,
                    message:'Not a valid phone number<br>(example: 123-456-7890)'
                }
            ];

            //add some sub-observables to our observable
            target.hasError = ko.observable();
            target.hasFocus = ko.observable();
            target.validationMessage = ko.observable();

            //define a function to do required and validate patterns if needed
            function check(newValue, start) {
                 if (options.required === true) {
                    target.hasError(newValue ? false : true);
                    target.hasFocus(newValue ? false : true);
                    // do not show message on load:

                    target.validationMessage(newValue ? "" : options.requiredMessage || "This field is required");
                    }

                //check for a test pattern type (i.e. email or phone) and for the target value
                if (options.pattern && newValue) {
                     //get the appropriate filter to test
                    var filter = $.grep(self.filters, function (item) {
                        return item.type == options.pattern
                    });
                    var pass = filter[0].pattern.test(newValue);
                    if (pass == false) {
                        target.hasError(true);
                        target.hasFocus(true);

                        target.validationMessage(filter[0].message)

                    } else {
                        target.hasError(false);
                        target.validationMessage("");
                    }
                }
               if (start){
                   //remove the validation message if this is a initial load
                   target.validationMessage("")
               }

            }

            //initial validation
            check(target(), start=true);

            //validate whenever the value changes
            target.subscribe(check);

            //return the original observable
            return target;
        };

    }


    utilities.validateKo = validateKo;


}(window.utilities));
/**
 *
 * User: jbennett
 * Date: 3/5/13
 * Time: 5:08 PM
 *
 */

(function (cartlogic){



function FormStep(id, name, template, model) {
    var self = this;
    self.id = id;
    self.name = ko.observable(name);
    self.template = template;
    self.model = ko.observable(model);

    self.getTemplate = function () {
        return self.template;
    }
}


//add to cartlogic name space
    cartlogic.FormStep = FormStep;

}(window.cartlogic));

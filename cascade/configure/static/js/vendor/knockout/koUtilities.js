/**
 *
 * User: jbennett
 * Date: 3/12/13
 * Time: 1:24 PM
 * Source: http://stackoverflow.com/questions/9877301/knockoutjs-observablearray-data-grouping
 * Used to filter an observable array by a distinct value on a property
 */


ko.observableArray.fn.distinct = function(prop) {
    var target = this;
    target.index = {};
    target.index[prop] = ko.observable({});

    ko.computed(function() {
        //rebuild index
        var propIndex = {};

        ko.utils.arrayForEach(target(), function(item) {
            var key = ko.utils.unwrapObservable(item[prop]);
            if (key) {
                propIndex[key] = propIndex[key] || [];
                propIndex[key].push(item);
            }
        });

        target.index[prop](propIndex);
    });

    return target;
};

/**
 *
 * User: jbennett
 * Date: 4/05/13
 * Time: 3:32 PM
 * Source: http://blog.pardahlman.se/2012/10/typeahead-from-twitter-bootstrap-data-bound-in-knockout-js/
 * Used with twitter bootstraps typeahead to auto complete
 */

ko.bindingHandlers.typeahead = {
    init: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
        var typeaheadSource; // <-- this is where our typeahead options will be stored in
        //this is the parameter that you pass from you data-bind expression in the mark-up
        var passedValueFromMarkup = ko.utils.unwrapObservable(valueAccessor());
        if (passedValueFromMarkup instanceof Array) typeaheadSource = passedValueFromMarkup;
        else {
            // if the name contains '.', then we expect it to be a property in an object such as myLists.listOfCards
            var splitedName = passedValueFromMarkup.split('.');
            var result = window[splitedName[0]];
            $.each($(splitedName).slice(1, splitedName.length), function(iteration, name) {
                result = result[name];
            });

            // if we find any array in the JsVariable, then use that as source, otherwise init without any specific source and hope that it is defined from attributes

            if (result != null && result.length > 0) {
                typeaheadSource = result;
            }

        }

        //jbennett - note the call to typeahead here  <ul class='typeahead dropdown-menu', style='z-index:150'></ul>
        if (typeaheadSource == null) $(element).typeahead();

        else {
           $(element).typeahead({
                source: typeaheadSource,
                items: 10
            });

        }


    }
};

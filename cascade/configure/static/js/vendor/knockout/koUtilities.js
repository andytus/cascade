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
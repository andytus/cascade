/**
 *
 * User: jbennett
 * Date: 5/3/13
 * Time: 3:56 PM
 *
 */


(function (cartlogic){

    function Comments(data) {
       var self = this;
       self.id = ko.observable();
       self.text = ko.observable();
       self.date_created = ko.observable();
       self.created_by = ko.observable();

       if (data){
       self.id(data.id);
       self.text(data.text);
       self.date_created(new Date(data.date_created).toDateString());
       self.created_by(data.created_by);

       }

    }

    cartlogic.Comments = Comments;


})(window.cartlogic);
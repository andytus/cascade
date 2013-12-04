/**
 *
 * User: jbennett
 * Date: 4/30/13
 * Time: 1:26 PM
 *
 */


(function (cartlogic) {


      function TicketsProfileViewModel(){
      var self = this;
       self.ticket = ko.observable();
       self.ticket_status_options = ko.observableArray([]);
       self.selected_status = ko.observable();
       self.ticket_comments = ko.observableArray([]);
       self.server_message_type = ko.observable();
       self.server_message = ko.observable();
       self.add_serial_number = ko.observable();


       self.getTicketComments = function(){
           $.getJSON(ticket_comment_api + ticket_id, function(data){
             if (!data.details){
                     var comments = $.map(data, function(item){
                     return new cartlogic.Comments(item)
                 });
                 self.ticket_comments(comments);
               }

           });
       };


       self.getServiceStatusOptions = function(){
           $.getJSON(ticket_status_api, function(data){
               var ticketStatusOptions = $.map(data, function (item) {
                  return new cartlogic.TicketStatusOption(item);

               });

               self.ticket_status_options(ticketStatusOptions);
               var match = ko.utils.arrayFirst(self.ticket_status_options(), function(item) {
                   return self.ticket().status__service_status() === item.service_status();
               });
               self.selected_status(match);

           });
       };

       self.getTicket = function(){
           $.getJSON(ticket_api + ticket_id, function(data){
               if (data.details){
                   $("#message-text").text(data.details.message);
                   $("#message").removeClass("alert-success").addClass('alert-error').show();
                   $('.close').click(function () {
                       $('#message').hide();
                   });

               } else{
               self.ticket(new cartlogic.Ticket(data));
               self.getServiceStatusOptions();
               }
           });

       };

      self.saveComment = function(){
          var new_comment = new cartlogic.Comments({text:$("[name=text]").val(), date_created: new Date(),  created_by: user_name});
          $.ajax(ticket_comment_api + ticket_id, {
                  data: ko.toJSON(new_comment),
                  type:"post", contentType:"application/json",
                  dataType:"jsonp",
                  success:function (data) {

                      self.server_message_type(data.details.message_type);
                      self.server_message(data.details.message);

                      $("#message-type").text(data.details.message_type +"! ");
                      $("#message-text").text(data.details.message);
                      $('.close').click(function () {
                          $('#message').hide();
                      });

                      if (data.details.message_type == 'Success'){
                          $("#message").removeClass("alert-error").addClass('alert-success').show();
                      } else{
                          $("#message").removeClass("alert-success").addClass('alert-error').show();
                      }


                      if(data.details.message_type == 'Success') {
                        //save the comment id to the new comment object
                       //needed for delete operation (i.e. save then delete in same page load)
                        new_comment.id = data.details.comment_id;
                        self.ticket_comments.push(new_comment);
                          $("[name=text]").val("")
                      }

                  },
                  error:function (data, jqXHR) {
                      //send error message to last step
                      self.server_message_type("ERROR!");
                      self.server_message(jqXHR.statusText)
                  }


              }
          );
     };

     self.deleteComment = function(comment){

         $.ajax(ticket_comment_api + ticket_id, {
                 data: ko.toJSON({'comment_id': comment.id}) ,
                 type:"delete", contentType:"application/json",
                 dataType:"jsonp",
                 success:function (data) {

                     $("#message-type").text(data.details.message_type +"! ");
                     $("#message-text").text(data.details.message);
                     $('.close').click(function () {
                         $('#message').hide();
                     });

                   if(data.details.message_type == 'Success') {
                        match_comment_id =self.ticket_comments().indexOf(comment);
                        self.ticket_comments.remove(comment);
                       $("#message").removeClass("alert-error").addClass('alert-success').show();
                     } else{
                       $("#message").removeClass("alert-success").addClass('alert-error').show();
                   }

                 },
                 error:function (data, jqXHR) {
                     $("#message").addClass("alert-error").show();
                     $("#message-type").text("Error! ");
                     $("#message-text").text(data.statusText);
                     $('.close').click(function () {
                         $('#message').hide();
                     });

                 }
             }
         );


     };

       self.updateTicket = function(status){
          cart_serial_number =  $("[name=add-serial-number]").val();
          $.ajax(ticket_api + ticket_id, {
              data: ko.toJSON({serial_number: cart_serial_number, status: status}),
              type:"post", contentType:"application/json",
              dataType:"jsonp",
              success:function (data) {
                  $("#message-type").text(data.details.message_type +"! ");
                  $("#message-text").text(data.details.message);
                  $('.close').click(function () {
                      $('#message').hide();
                  });

                  if(data.details.message_type == 'Success') {

                      self.getTicket();

                     /*self.ticket().success_attempts(self.ticket().success_attempts() + 1);
                     self.ticket().updated_by(user_name);
                     self.ticket().processed("true");*/


                      $("#message").removeClass("alert-error").addClass('alert-success').show();
                  } else{
                      $("#message").removeClass("alert-success").addClass('alert-error').show();
                  }

              },
              error:function (data, jqXHR) {
                  //send error message to last step
                  $("#message").addClass("alert-error").show();
                  $("#message-type").text("Error! ");
                  $("#message-text").text(data.statusText);
                  $('.close').click(function () {
                      $('#message').hide();
                  });

              }


           });

       };

          self.confirmDeleteTicket = function(){
              $("#confirm_delete_ticket").html("Are you sure you want to delete <b> " + self.ticket().id() + "</b>?" );
              $("#delete_confirm").modal("show");
          }


          self.deleteTicket = function(status){
              $.ajax(ticket_api + ticket_id, {
                  data: ko.toJSON({status: status}),
                  type:"DELETE", contentType:"application/json",
                  dataType:"jsonp",
                  success:function (data) {
                      $("#message-type").text(data.details.message_type +"! ");
                      $("#message-text").text(data.details.message);
                      $('.close').click(function () {
                          $('#message').hide();
                      });

                      if(data.details.message_type == 'Success') {
                          $("#ticket-profile").html('');
                          $("#message").removeClass("alert-error").addClass('alert-success').show();
                      } else{
                          $("#message").removeClass("alert-success").addClass('alert-error').show();
                      }

                  },
                  error:function (data, jqXHR) {
                      //send error message to last step
                      $("#message").addClass("alert-error").show();
                      $("#message-type").text("Error! ");
                      $("#message-text").text(data.statusText);
                      $('.close').click(function () {
                          $('#message').hide();
                      });

                  }


              });

          };


      self.getTicket();
      self.getTicketComments();

      }


    cartlogic.TicketsProfileViewModel = TicketsProfileViewModel;

})(window.cartlogic);
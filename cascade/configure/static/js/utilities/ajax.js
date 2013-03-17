/**
 *
 * User: jbennett
 * Date: 3/15/13
 * Time: 9:09 AM
 *
 */


window.utilities = {};

(function(utilities){

 // The following set of utility functions are used to protect Ajax calls from cross-site forgery attacks

    //Get Cookie with TOKEN FOR AJAX QUERIES
    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
   // add to utilities name space
    utilities.getCookie = getCookie;

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    // add to utilities name space
    utilities.csrfSafeMethod = csrfSafeMethod;


    function setupAjax(){
    var csrftoken = utilities.getCookie('csrftoken');

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!utilities.csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
     })
    }

    utilities.setupAjax = setupAjax;
 ///////////////////////////////////////////////////////////////////////////////////////////////////////////


}(window.utilities));

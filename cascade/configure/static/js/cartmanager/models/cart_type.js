/**
 *
 * User: jbennett
 * Date: 3/3/13
 * Time: 6:34 PM
 *
 */


(function (cartlogic){

    function TypeOption(data) {
        this.id = data.id;
        this.name = data.name;
        this.size = data.size;
        this.site =data.site;
    }
    cartlogic.TypeOption = TypeOption;

})(window.cartlogic);
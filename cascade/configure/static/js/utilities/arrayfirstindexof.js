

(function (cartlogic){
//solutions from: http://stackoverflow.com/questions/6926155/how-to-use-indexof-in-knockoutjs
function arrayFirstIndexOf(array, predicate, predicateOwner) {
    for (var i = 0, j = array.length; i < j; i++) {
        if (predicate.call(predicateOwner, array[i])) {
            return i;
        }
    }
    return -1;
}
 cartlogic.arrayFirstIndexOf = arrayFirstIndexOf;

}(window.cartlogic));
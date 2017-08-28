$(document).ready(function() {
    var serverAddr = "http://localhost:8000/pkw/";

    $(document).ajaxError(function(){
        alert("An error occurred!");
    });

    function loadArea(data) {
        $("tbody,#child_name,#child_name_plural,title,.pageheader").empty();
    }

    function makeAreaGetter(areaType, pk) {
        return function() {
            $.getJSON(serverAddr + areaType, function(result) {
                loadArea(result);
                localStorage.setItem("pkw_area", result);
            });
        }
    }


    var oldData = localStorage.getItem("pkw_area");
    if(oldData != null) {
        loadArea(oldData);
    }

    makeAreaGetter('country', 'Polska')();
});

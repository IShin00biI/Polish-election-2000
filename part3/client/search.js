$(document).ready(function() {
    var requestAddr = pkw.serverAddr + "search/";

    function loadResults(results) {
        var node = $("#results").empty().show();
        var curr_link;
        if(!$.isEmptyObject(results)) {
            node = node.text("Wyniki").append($("<ul>")).find("ul");
            for(var pk in results) {
                curr_link = node.append($("<li>")
                    .append($("<a>")
                        .text(results[pk] + " (" + pk + ")")))
                    .find("a:last");
                curr_link.attr("href", "./area.html?areatype=commune&pk=" + pk)
            }
        }
        else {
            node.text("Brak wyników.");
        }
    }

    pkw.setUpErrors();

    pkw.refreshLogStripe();

    $("#search_button").click(function(e) {
        e.preventDefault();
        query = $("#search_input").val();
        if(query === "") {
            alert("Wypełnij polę wyszukiwania!");
            return;
        }
        $.get(requestAddr,
            { search: query },
            function(data) {
                if(data === "INVALID") {
                    alert("Serwer otrzymał niepoprawne zapytanie!");
                    return;
                }
                $("#query_display").show().find("span").text(query);
                loadResults(data);
            });
    });

});

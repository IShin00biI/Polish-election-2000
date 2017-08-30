$(document).ready(function() {

    function createSubmitFunction(areaType, pk) {
        return function(e) {
            e.preventDefault();
            var username = localStorage.getItem("pkw_username");
            var password = localStorage.getItem("pkw_password");
            if(username && password) {
                var serializedForm = $("#cand_form").serialize();
                serializedForm += "&username=" + username + "&password=" + password;
                if(serializedForm.search("=&") !== -1) {
                    alert("Wypełnij wszystkie pola!");
                    return;
                }

                if(!areaType || !pk) areaType = pk = '';

                $.post(pkw.serverAddr + areaType + pk,
                    serializedForm,
                    function(result) {
                        if(result === "OK") {
                            createAreaLoader(areaType, pk)();
                            alert("OK");
                        }
                        else if(result === "DENIED")
                            alert("Odmowa dostępu! Zaloguj się ponownie.");
                        else
                            alert("Dane w formularzu są nieprawidłowe!");
                    });
            }
            else {
                alert("Błędne dane logowania! Zaloguj się ponownie.");
            }
        };
    }

    function loadArea(data, areaType, pk) {
        pkw.refreshLogStripe(loadArea, data);
        data = JSON.parse(data);

        var cand, child;

        $("tbody,#child_name,#child_name_plural,title,.pageheader > h1,.pageheader a," +
            "#children_section thead,title").empty();
        $("title").text(data.area + " - PKW2000");
        $(".pageheader > h1").text(data.area);
        $("#child_name_plural").text(data.child_name_plural);
        $("#refresh").unbind("click").click(createAreaLoader(areaType, pk));

        if(data.parent && data.parent_type) {
            $(".pageheader a").unbind("click")
                .click(createAreaLoader(data.parent_type, data.parent))
                .text(data.parent_name_full);
        }

        $.each(data.stat_list, function(i, stat) {
            if(data.stats.hasOwnProperty(stat)) {
                $("#stat_table").find("tbody")
                    .append($("<tr>")
                        .append($("<td>")
                            .text(stat)
                        )
                        .append($("<td>")
                            .text(data.stats[stat])
                        )
                    )
            }
        });

        var enableForm = username && $.isEmptyObject(data.children);

        for(cand in data.candidates) {
            if(data.candidates.hasOwnProperty(cand)) {
                $("#cand_table_body")
                    .append($("<tr>")
                        .append($("<td>")
                            .text(data.candidate_names[cand])
                        )
                        .append($("<td>")
                            .html(
                                enableForm
                                    ? '<input type="number" name="'
                                        + cand + '" value="' + data.candidates[cand] + '">'
                                    : data.candidates[cand]
                            )
                        )
                        .append($("<td>")
                            .text(Math.round((data.candidates[cand]
                                / data.stats["Głosy ważne"]) * 10000) / 100 + "%")
                        )
                    )
            }
        }

        if(enableForm)
            $("#cand_table_body")
                .append($("<tr>")
                    .append($("<td>")
                        .append($("<button>")
                            .text("Zapisz")
                            .click(createSubmitFunction(areaType, pk))
                        )
                    )
                );

        var childrenSection = $("#children_section");

        if($.isEmptyObject(data.children))
            childrenSection.hide();
        else {
            childrenSection.show();
            var tableHead = childrenSection.find("thead");
            tableHead = tableHead
                .append($("<tr>")
                    .append($("<th>")
                        .text(data.child_name)))
                .find("tr");

            $.each(data.stat_list, function(i, stat) {
                tableHead.append($("<th>").text(stat));
            });

            var tableBody = childrenSection.find("tbody");
            for(child in data.children) {
                if(data.children.hasOwnProperty(child)) {
                    tableBody.append($("<tr>")
                        .append($("<td>")
                            .append($("<a>")
                                .click(createAreaLoader(data.child_type, child))
                                .text(child)
                            )
                        )
                    );
                }

                var tableRow = tableBody.find("tr:last");
                $.each(data.stat_list, function(i, stat) {
                    tableRow.append($("<td>").text(data.children[child][stat]));
                });
            }
        }
    }

    function createAreaLoader(areaType, pk) {
        if(!areaType || !pk) areaType = pk = '';
        else if(areaType.charAt(areaType.length - 1) !== "/") areaType += "/";
        return function() {
            $.get(pkw.serverAddr + areaType + pk, function(result) {
                loadArea(result, areaType, pk);
                localStorage.setItem("pkw_area", result);
            }, "text");
        }
    }

    function parseParameters() {
        var searchString = window.location.search.substring(1);
        var params = searchString.split("&");
        var i, pair;
        var result = {};

        for (i=0; i<params.length; i++) {
            pair = params[i].split("=");
            result[pair[0]] = pair[1];
        }
        return result;
    }

    pkw.setUpErrors();

    $("#index_link").click(createAreaLoader());

    var oldData = localStorage.getItem("pkw_area");
    if(oldData) {
        loadArea(oldData);
    }

    var parameters = parseParameters();

    if(parameters.areatype && parameters.pk)
        createAreaLoader(parameters.areatype, parameters.pk)();
    else
        createAreaLoader()();

});

$(document).ready(function() {

    function getSubmitFunction(areaType, pk) {
        return function(e) {
            e.preventDefault();
            var username = localStorage.getItem("pkw_username");
            var password = localStorage.getItem("pkw_password");
            if(username && password) {
                var serializedForm = $("#cand_form").serialize();
                serializedForm += "&username=" + username + "&password=" + password;
                if(serializedForm.search("=&") !== -1) {
                    $(".errormsg").show().text("Wypełnij wszystkie pola!");
                    return;
                }

                if(!areaType || !pk) areaType = pk = '';

                $.post(pkw.serverAddr + areaType + pk,
                    serializedForm,
                    function(result) {
                        if(result === "OK") {
                            makeAreaGetter(areaType, pk)();
                            alert("OK");
                        }
                        else if(result === "DENIED")
                            $(".errormsg").show().text("Odmowa dostępu! Zaloguj się ponownie.");
                        else
                            $(".errormsg").show().text("Dane w formularzu są nieprawidłowe!");
                    });
            }
            else {
                $(".errormsg").show().text("Błędne dane logowania! Zaloguj się ponownie.");
            }
        };
    }

    function loadArea(data, areaType, pk) {
        pkw.refreshLogStripe(loadArea, data);
        data = JSON.parse(data);
        $("tbody,#child_name,#child_name_plural,title,.pageheader > h1,#children_section thead tr,.errormsg").empty();
        $(".errormsg").hide();
        $(".pageheader > h1").text(data.area);
        $("#child_name_plural").text(data.child_name_plural);

        var cand = null;

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
                                    ? '<input type="number" name="' + cand + '" value="' + data.candidates[cand] + '" required>'
                                    : data.candidates[cand]
                            )
                        )
                        .append($("<td>")
                            .text(Math.round((data.candidates[cand] / data.stats["Głosy ważne"]) * 10000) / 100 + "%")
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
                            .click(getSubmitFunction(areaType, pk))
                        )
                    )
                );

        var childrenSection = $("#children_section");

        if($.isEmptyObject(data.children))
            childrenSection.hide();
        else {
            childrenSection.show();
            tableHead = childrenSection.find("thead tr");
            tableHead.append($("<th>").text(data.child_name));

            $.each(data.stat_list, function(i, stat) {
                tableHead.append($("<th>").text(stat));
            });

            tableBody = childrenSection.find("tbody");
            for(child in data.children) {
                tableBody.append($("<tr>")
                    .append($("<td>")
                        .append($("<a>")
                            .click(makeAreaGetter(data.child_type, child))
                            .text(child)
                        )
                    )
                );

                tableRow = tableBody.find("tr:last");
                $.each(data.stat_list, function(i, stat) {
                    tableRow.append($("<td>").text(data.children[child][stat]));
                });
            }
        }
    }

    function makeAreaGetter(areaType, pk) {
        if(!areaType || !pk) areaType = pk = '';
        else if(areaType.charAt(areaType.length - 1) !== "/") areaType += "/";
        return function() {
            $.get(pkw.serverAddr + areaType + pk, function(result) {
                loadArea(result, areaType, pk);
                localStorage.setItem("pkw_area", result);
            }, "text");
        }
    }

    pkw.setUpErrors();

    $("#index_link").click(makeAreaGetter());

    var oldData = localStorage.getItem("pkw_area");
    if(oldData) {
        loadArea(oldData);
    }

    makeAreaGetter()();
});

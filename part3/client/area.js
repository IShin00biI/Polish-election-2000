$(document).ready(function() {

    function loadArea(data) {
        pkw.refreshLogStripe(loadArea, data);
        data = JSON.parse(data);
        $("tbody,#child_name,#child_name_plural,title,.pageheader > h1,#children_section thead tr").empty();
        $(".pageheader > h1").text(data.area);
        $("#child_name_plural").text(data.child_name_plural);

        $.each(data.stat_list, function(i, stat) {
            if(data.stats.hasOwnProperty(stat)) {
                $("#stat_table").find("tbody")
                    .append($("<tr></tr>")
                        .append($("<td></td>")
                            .text(stat)
                        )
                        .append($("<td></td>")
                            .text(data.stats[stat])
                        )
                    )
            }
        });

        var enableForm = username && $.isEmptyObject(data.children);

        for(cand in data.candidates) {
            if(data.candidates.hasOwnProperty(cand)) {
                $("#cand_table").find("tbody")
                    .append($("<tr></tr>")
                        .append($("<td></td>")
                            .text(data.candidate_names[cand])
                        )
                        .append($("<td></td>")
                            .text(data.candidates[cand])
                        )
                        .append($("<td></td>")
                            .text(Math.round((data.candidates[cand] / data.stats["Głosy ważne"]) * 10000) / 100 + "%")
                        )
                    )
            }
        }

        var childrenSection = $("#children_section");

        if($.isEmptyObject(data.children))
            childrenSection.hide();
        else {
            childrenSection.show();
            tableHead = childrenSection.find("thead tr");
            tableHead.append($("<th></th>").text(data.child_name));

            $.each(data.stat_list, function(i, stat) {
                tableHead.append($("<th></th>").text(stat));
            });

            tableBody = childrenSection.find("tbody");
            for(child in data.children) {
                tableBody.append($("<tr></tr>")
                    .append($("<td></td>")
                        .append($("<a></a>")
                            .click(makeAreaGetter(data.child_type, child))
                            .text(child)
                        )
                    )
                );

                tableRow = tableBody.find("tr:last");
                $.each(data.stat_list, function(i, stat) {
                    tableRow.append($("<td></td>").text(data.children[child][stat]));
                });
            }
        }
    }

    function makeAreaGetter(areaType, pk) {
        if(!areaType || !pk) areaType = pk = '';
        else areaType += "/";
        return function() {
            $.get(pkw.serverAddr + areaType + pk, function(result) {
                loadArea(result);
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

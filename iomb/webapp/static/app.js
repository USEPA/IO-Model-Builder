'use strict';

function fillTable() {
    var t = $.templates("<tr><td>{{:name}}</td><td>{{:location}}</td><td></td></tr>");
    $.get("/api/sectors", function (sectors) {
        var html = '';
        $.each(sectors, function (idx, sector) {
            html += t.render(sector);
        });
        $('#demand-table').append(html);
    });
}

$(function () {
    fillTable();
    $('#calc-btn').click(function () {
        $.get("/api/sectors", function (data) {
            console.log(data)
        });
    });
});

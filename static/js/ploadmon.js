var _memchart = 0;
var _corechart = 0;

function fillstatstable(s) {
    var tdata = "";
    $.each(s, function (a, i) {
        tdata += ("<tr><td>" + i[0] + "</td><td>" + i[1] + "</td></tr>/n");
        $('#statstable').html(tdata);
    });


}

function getserverstats() {

    $.get("/stats", function (data) {

        $('#waiter').hide();
        $('#maingrid').show();

        if (_memchart == 0) {
            _memchart = new Morris.Area(data['memchart'])
        }
        if (_corechart == 0) {
            _corechart = new Morris.Line(data['corechart'])
        }

        new Morris.Donut(data['memdognut']);
        new Morris.Donut(data['hdddognut']);

        if (_corechart !== 0 && _memchart !== 0) {
            _memchart.setData(data["memchart"]["data"]);
            _corechart.setData(data["corechart"]["data"]);
        }
        fillstatstable(data["serverstatus"]);


    });

}


function managesize() {
    var baseheight = $(window).height() - $("#footer").height() - $("#header").height();
    $("#waiter").height(baseheight / 1.3);
    $("#memgraph").height(baseheight / 3);
    $("#coresgraph").height(baseheight / 3);
    $("#memdognut").height(baseheight / 3);
    $("#hdddognut").height(baseheight / 3);
    $("#main").height(baseheight);
}


$(document).ready(function () {
    managesize();
    getserverstats();
    setInterval(function () {
        getserverstats();
    }, 5000);


    $(window).on('resize', function () {
        $('#maingrid').hide();
        $('#waiter').show();

    });

});
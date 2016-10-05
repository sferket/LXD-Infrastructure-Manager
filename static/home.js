
function update_memory_progressbar(s) {
    pb_id = "#" + s + "_progress"; 
    total_id = "#" + s + "_memtotal";
    free_id = "#" + s + "_memfree";
    total = $(total_id).text();
    free = $(free_id).text();
    total_int = parseInt(total, 10);
    free_int = parseInt(free, 10);
    prcnt = Math.floor((free_int / total_int) * 100);
    prcnt_str = prcnt.toString(); 
    $(pb_id).attr("aria-valuenow",prcnt_str);
    $(pb_id).css("width",prcnt_str + "%");
}

setTimeout(update_memory_progressbar("server_one"),1000);

function on_click_server(s) {
    pnl = "#collapse_" + s; 
    s_info = "#" + s + "_server_info";
    $("#info_div").children().hide();
    if ($(pnl).hasClass("in")) {
       $(s_info).hide(); 
    }
    else {
       $(s_info).show(); 
    }
    //update_memory_progressbar(s);
}

function on_click_container(s,c) {
    $("#info_div").children().hide();
    container_id = "#" + s + "_" + c + "_container_info";
    $(container_id).toggle();
}

function on_click_cmd(s, c, cmd) {
    var cmd_url = "/cmd/" + s + "/" + c + "/" + cmd;
    $.ajax({
        url: cmd_url,
        type: "GET",
    })
        .done(function() {
            var container_info;
            var tr = "#" + s + "_" + c + "_trr";
            var si = "#" + s + "_server_info";
            $.ajax({
                url: "/update/container/info/",
                type: "GET",
                success: function(data) { 
                    console.log("Data: " + data["server_one"]);
                    //var server_info = data[s];
                    console.log("Server info: " + data[s]);
                    for (var i=0; i<data[s].length; i++){
                         if ( data[s][i]["name"] == c ) {
                            var server_status = data[s][i]["status"];
                            var status_td = "#" + s + "_" + c + "_status";
                            var status_info = "#" + s + "_" + c + "_status_info";
                            var status_span = "#" + s + "_" + c + "_status_span";
                            var status_code = "#" + s + "_" + c + "_status_code";
                            $(tr).attr("class", server_status + "_bg");
                            $(status_td).text(server_status);
                            console.log("server status: " + server_status);
                            $(status_code).text(data[s][i]["status_code"]);
                            if (server_status == "Running") { 
                                console.log("running");
                                var h = "<span class='label label-success'>" + server_status + "</span>";
                                $(status_info).html(
                                    h
                                );
                            }
                            else if (server_status == "Frozen") {
                                console.log("frozen");
                                var h = "<span class='label label-info'>" + server_status + "</span>";
                                $(status_info).html(
                                    h
                                );
                            }
                            else {
                                var h = "<span class='label label-danger'>" + server_status + "</span>";
                                console.log("danger");
                                $(status_info).html(
                                    h
                                );
                            }
                            set_button_activity(s,c,server_status);
                         }
                    }
                },
            })
        });
}

function set_button_activity(s,c,state){
    var start_button = "#" + s + "_" + c + "_startbutton";
    var stop_button = "#" + s + "_" + c + "_stopbutton";
    var freeze_button = "#" + s + "_" + c + "_freezebutton";
    var unfreeze_button = "#" + s + "_" + c + "_unfreezebutton";
    var start_button_ct = "#" + c + "_" + s + "_startbutton";
    var stop_button_ct = "#" + c + "_" + s + "_stopbutton";
    var freeze_button_ct = "#" + c + "_" + s + "_freezebutton";
    var unfreeze_button_ct = "#" + c + "_" + s + "_unfreezetbutton";
    if(state=="Running"){
        $(start_button).attr("class","btn btn-default disabled");
        $(stop_button).attr("class","btn btn-default");
        $(freeze_button).attr("class","btn btn-default");
        $(unfreeze_button).attr("class","btn btn-default disabled");
        $(start_button_ct).attr("class","btn btn-default disabled");
        $(stop_button_ct).attr("class","btn btn-default");
        $(freeze_button_ct).attr("class","btn btn-default");
        $(unfreeze_button_ct).attr("class","btn btn-default disabled");
    }
    else if(state=="Stopped"){
        $(start_button).attr("class","btn btn-default");
        $(stop_button).attr("class","btn btn-default disabled");
        $(freeze_button).attr("class","btn btn-default disabled");
        $(unfreeze_button).attr("class","btn btn-default disabled");
        $(start_button_ct).attr("class","btn btn-default");
        $(stop_button_ct).attr("class","btn btn-default disabled");
        $(freeze_button_ct).attr("class","btn btn-default disabled");
        $(unfreeze_button_ct).attr("class","btn btn-default disabled");
    }
    else if(state=="Frozen"){
        $(start_button).attr("class","btn btn-default disabled");
        $(stop_button).attr("class","btn btn-default disabled");
        $(freeze_button).attr("class","btn btn-default disabled");
        $(unfreeze_button).attr("class","btn btn-default");
        $(start_button_ct).attr("class","btn btn-default disabled");
        $(stop_button_ct).attr("class","btn btn-default disabled");
        $(freeze_button_ct).attr("class","btn btn-default disabled");
        $(unfreeze_button_ct).attr("class","btn btn-default");
    }
}


var initial_setup_charts = true;
var myCharts = {};

function setup_chart(server) {
    console.log("set_chart");
    var chart_id = s + "_chart_container";
    var ctx = document.getElementById(chart_id);
    myCharts[server] = new Chart(ctx, {
        type: 'line',
        label: "Cpu usage per server",
        data: {
            labels: [],
            datasets: [
                {
                    label: s,
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(75,192,192,0.4)",
                    borderColor: "rgba(75,192,192,1)",
                    borderCapStyle: "butt",
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: "miter",
                    pointBorderColor: "rgba(75,192,192,1)",
                    pointBackgroundColor: "#fff",
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgba(75,192,192,1)",
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: [65, 40, 23, 54, 34, 90, 45],
                    spanGaps: false,
                }
            ]
        }
    });
}
var update_graph = function(data) {
    if (initial_setup_charts) {
        for (s in data) {
            setup_chart(s);
        }
        initial_setup_charts = false;
    }
    for (s in data) {
        var chart_id = s +"_chart_container";
        var ctx = document.getElementById(chart_id);
        var cpu_datasets = []
        var cpu_label_ticks = []
        var server_cpu_data = data[s]["data"];
        for (c in server_cpu_data) {
            var cpu_data = {
                label: s,
                fill: false,
                lineTension: 0.1,
                backgroundColor: data[s]["color"],
                borderColor: data[s]["color"],
                borderCapStyle: "butt",
                borderDash: [],
                borderDashOffset: 0.0,
                borderJoinStyle: "miter",
                pointBorderColor: "rgba(75,192,192,1)",
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: "rgba(75,192,192,1)",
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: server_cpu_data[c],
                spanGaps: false,
            }      
            cpu_datasets = cpu_datasets.concat(cpu_data);
            label_ticks = data[s]["labels"][c];
        }
        myCharts[s].data.xLabels = label_ticks;
        myCharts[s].data.datasets = cpu_datasets;
        myCharts[s].update(0,0);
    }
    };

$(document).ready(function(){
    namespace = "/update";
    var socket = io.connect(
        "http://" 
        + document.domain 
        + ":" 
        + location.port 
        + namespace
    );

    socket.on("connect", function(msg) {
        socket.emit("got event", {data: "Im connected!"});
    });


    socket.on("message", function(msg) {
        update_graph(msg.cpu_usage);
    });

});


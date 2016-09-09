
function update_memory_progressbar(s) {
    console.log("update_memory");
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

/*
function on_click_server(s){
    pnl = "#collapse_" + s;
    tr = "." + s + "_tr";
    server_info_div = "#" + s + "_server_info_div";

    if ($(pnl).hasClass("in")) {
        $(tr).css("display","none");
        $(server_info_div).css("display","none");
    }
    else {
        $(tr).css("display","table-row");
        $(server_info_div).css("display","block");
        update_memory_progressbar(s);
    }
}

function on_click_cmd(s,c,cmd) {
    var cmd_url = "/cmd/" + s + "/" + c + "/" + cmd;
    console.log("cmd_url: " + cmd_url);
    $.ajax({
        url: cmd_url,
        type: "GET",
    })
    console.log("post-ajax");
    $("#server_info_table").load("/" + " #actual_table");
    var z = "#collapse_" + s;
    var y = " ." + s + "_tr";
    $(z).addClass("in");
    console.log("on click 2");
    $("#actual_table").load("/" + y);
    console.log("done");
}

function on_click_cont(c) {
    console.log("c: " + c);
    $("#server_info_table").css("display","none");
    var cont_divs =  document.getElementsByClassName("container_info");
    for (var i=0; i<cont_divs.length; i++) {
        cont_divs[i].style.display = "None";
    }
    c_id = "#" + c + "_cont_info";
    $(c_id).css("display","block");
}

function update_memory_progressbar(s) {
    pb_id = "#" + s + "_progress"; 
    total_id = "#" + s + "_memtotal";
    free_id = "#" + s + "_memfree";
    total = $(total_id).text();
    free = $(free_id).text();
    total_int = parseInt(total, 10);
    free_int = parseInt(free, 10);
    prcnt = 100 - Math.floor((free_int / total_int) * 100);
    prcnt_str = prcnt.toString(); 
    $(pb_id).attr("aria-valuenow",prcnt_str);
    $(pb_id).css("width",prcnt_str + "%");
    $(pb_id).text(prcnt_str + "%");
}
*/

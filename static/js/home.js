function container_action(button) {
    var server_info = button.childNodes[1].innerText;
    //server_info = server_info.split(";");
    $.ajax({
        url: "/container_cmd/",
        type: "POST",
        data: JSON.stringify({
            "info": server_info,
        }),
        contentType: "application/json",
        dataType: "json",
    });
}

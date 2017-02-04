app.directive("detailsServer", ["$http", function($http) {
	return {
        restrict: "E",
        scope: {
            server: "=server",
            containers: "=containers",
//            server_info: "=serverinfo",	
        },
        templateUrl: "/static/js/directives/details_server.html",
        
        link: function($scope, elem, attr) {
            $scope.runContainerMethod = function(server, container, method) {
                console.log("runcontainermethod");
                var data = {
                    "server": server.servername,
                    "container": container.name,
                    "method": method,
                    "type": "container"
                };
                data = JSON.stringify(data);
                var config = {
                    headers: {
                        "Content-Type": "application/json",
                    }
                }
                $http.post("/container_cmd/", data, config)
                    .success(function (data, status, headers, config) {
                        container.status = data["status"];
                    })
                    .error(function (data, status, header, config) {
                        console.log("error");
                    });
            };
        }
    }
}]);


$( document ).ready(function() {
    namespace = "/update";
    var socket = io.connect(
        "http://" 
        + document.domain 
        + ":" 
        + location.port 
        + namespace
    );

    socket.on("connect", function(msg) {
    	console.log("socket.on");
        socket.emit(
            "connected", 
            {data: "Im connected!",}
        );
    });

    socket.on('disconnect', function(){
        console.log('user disconnected');
    });    
    
    socket.on('my_response', function(msg) {
        if (document.getElementById("server-name")){
        	server = document.getElementById("server-name").value;
        	mes = JSON.parse(msg)
        	$('#test-test').text(mes['localhost']['tmp']);
        	$('#lsb_release').text(mes[server]['lsb_release']);
        	$('#uptime').text(mes[server]['uptime']);
        	$('#cpu').text(mes[server]['cpu']);
        	$('#avg1').text(mes[server]['avg1']);
        	$('#avg5').text(mes[server]['avg5']);
        	$('#avg15').text(mes[server]['avg15']);
        	$('#MemTotal').text(mes[server]['MemTotal']);
        	$('#MemAvailable').text(mes[server]['MemAvailable']);
        	$('#MemFree').text(mes[server]['MemFree']);
        	$('#SwapTotal').text(mes[server]['SwapTotal']);
        	$('#SwapFree').text(mes[server]['SwapFree']);
        	$('#iowait').text(mes[server]['iowait']);
        }
        
        //console.log(server);
        //$('#ping-pong').text(msg[server]);
    });

    socket.on('destroy', function () {
    	console.log("Destroy");
        socket.removeListener('my_response');
    });    
//    socket.on("update_graph", function(msg) {
//        update_graph(msg.cpu_usage);
//    });
});

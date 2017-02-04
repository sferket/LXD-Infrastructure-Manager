app.directive("detailsServer", ["$http", function($http) {
	return {
        restrict: "E",
        scope: {
            server: "=server",
            containers: "=containers",
            disks: "=disks"
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
                        console.log('TEst 123')
                    })
                    .error(function (data, status, header, config) {
                        console.log("error");
                    });
            };
        }
    }
}]);


//$( document ).ready(function() {
//    namespace = "/update";
//    var socket = io.connect(
//        "http://" 
//        + document.domain 
//        + ":" 
//        + location.port 
//        + namespace
//    );
//
//    socket.on("connect", function(msg) {
//    	console.log("socket.on");
//        socket.emit(
//            "connected", 
//            {data: "Im connected!",}
//        );
//    });
//
//    socket.on('disconnect', function(){
//        console.log('user disconnected');
//    });    
//    
//    function loadTable(tableId, fields, data) {
//        //$('#' + tableId).empty(); //not really necessary
////    	<div class="col-xs-10 col-xs-offset-1 center" ng-repeat="c in containers | orderBy:'status'" style="border-bottom:1px solid black;">
////        <div class="col-xs-2">
////            <h5>[[c.name]]</h5>
////        </div>
//        
//        var rows = '';
//        $.each(data, function(index, item) {
//            var row = '<div class="col-xs-10 col-xs-offset-1 center" style="border-bottom:1px solid black;">';
//            $.each(fields, function(index, field) {
//            	if (field == 'Use%') {
//            		row += 	
//            		'<h5><div class="progress">' +
//            		'  <div class="progress-bar progress-bar-success" role="progressbar"' +
//            		'  aria-valuenow="" aria-valuemin="0" aria-valuemax="100" style="width:' + item[field+''] + '">' +
//            		item[field+''] +
//            		'  </div>' +
//            		'</div></h5>' ;
//            	} else {
//            		row += '<div class="col-xs-2"><h5>' + item[field+''] + '</h5></div>';
//            	}
//                
//            	//row += '<td>' + 'Hobby' + '</td>';
//            });
//            rows += row + '</div>';
//        });
//        $('#' + tableId).html(rows);
//    }    
//    socket.on('my_response', function(msg) {
//    	console.log('response1')
//    	
//
//    	if (document.getElementById("server-name_tmp")){
//        	server = document.getElementById("server-name").value;
//        	mes = JSON.parse(msg)
//        	$('#test-test').text(mes['localhost']['tmp']);
//        	$('#lsb_release').text(mes[server]['lsb_release']);
//        	$('#uptime').text(mes[server]['uptime']);
//        	$('#cpu').text(mes[server]['cpu']);
//        	$('#avg1').text(mes[server]['avg1']);
//        	$('#avg5').text(mes[server]['avg5']);
//        	$('#avg15').text(mes[server]['avg15']);
//        	$('#MemTotal').text(mes[server]['MemTotal']);
//        	$('#MemAvailable').text(mes[server]['MemAvailable']);
//        	$('#MemFree').text(mes[server]['MemFree']);
//        	$('#SwapTotal').text(mes[server]['SwapTotal']);
//        	$('#SwapFree').text(mes[server]['SwapFree']);
//        	$('#iowait').text(mes[server]['iowait']);
////        	$('#disks').text(mes[server]['disks']);
//        	loadTable('data-table', ['Mounted on', 'Size', 'Use%'], mes[server]['disks']);
//        	
//        	
//        }
//        
//        //console.log(server);
//        //$('#ping-pong').text(msg[server]);
//    });
//
//    socket.on('destroy', function () {
//    	console.log("Destroy");
//        socket.removeListener('my_response');
//    });    
////    socket.on("update_graph", function(msg) {
////        update_graph(msg.cpu_usage);
////    });
//});

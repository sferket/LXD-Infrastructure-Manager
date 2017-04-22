app.controller("MainController", ["$scope", "$http", "$compile", 
function($scope, $http, $compile) {
	
    $scope.servers = null,
    $scope.server = null,
    $scope.server_info = null,
    $scope.containers = null,
    $scope.container = null,
    // Get data from server when loading page
    $http({
        method: "GET",
        url: "/get_info"
    })
        .then(
            function Success(response) {
                $scope.servers = response.data.servers;
                $scope.server_info = response.data.server_info;
                $scope.containers = response.data.containers;
                //$scope.sections = response.data.sections;
                
                console.log("response: ", response);
                console.log("servers: ", $scope.servers);
                console.log("server_info: ", $scope.server_info);
                console.log("containers: ", $scope.containers);
            },
            function Error(response) {
                console.log("Error getting data");
            }
        ),
    $scope.updateData = function() {
        console.log("updating updateData")
        $http({
            method: "GET",
            url: "/get_info"
        })
        .then(
            function Success(response) {
                $scope.servers = response.data.servers;
                //$scope.servers = '';
                $scope.server_info = response.data.server_info;
                $scope.containers = response.data.containers;
                $scope.sections = response.data.sections;
                
//                console.log("response: ", response);
//                console.log("servers: ", $scope.servers);
//                console.log("server_info: ", $scope.server_info);
//                console.log("containers: ", $scope.containers);
//                console.log("sections: ", $scope.sections);
            },
            function Error(response) {
                console.log("Error getting data");
            }
        )
    },
    // Get functions
    $scope.getContainersByServer = function(servername) {
        return $scope.containers[servername];
    },
    $scope.getServerByName = function(name) {
//    	console.log('=>')
//    	console.log($scope.servers[name])
        return $scope.servers[name];
    },
//    $scope.getServerInfoByName = function(name) {
//        return $scope.server_info[name];
//    },
    $scope.getContainerByName = function(server, name) {
    	console.log('===>', name )
        var containers = $scope.getContainersByServer(server);
    	var servers = $scope.servers
//    	console.log('1>', servers[server])
//    	console.log('2>', servers[server]['lxd_container_get'])
//    	console.log('3>', servers[server]['lxd_container_get']['test123'])
//    	console.log('3.1>', servers[server]['lxd_snapshots_all'])
        for (c_index in servers[server]['lxd_container_get']){
//        	console.log('4>', c_index)
//        	console.log('4>', servers[server]['lxd_container_get'][c_index][name])
        	
            if (name in servers[server]['lxd_container_get'][c_index]) {
            	ret = servers[server]['lxd_container_get'][c_index][name]; 
            	//ret['snapshots'] = servers[server]['lxd_snapshots_all'][c_index][name];
            	ret['snapshots'] = servers[server]['lxd_snapshots_all'][name]
                return ret;
            }
        }
    	
//    	return servers[server]['lxd_container_get']['test123']
//        for (c_index in containers){ 
//            if (containers[c_index].name == name) {
//                return containers[c_index];
//            }
//        }
    },
    // Load detail directives on menu item click 
    $scope.openDetailsContainer = function(server, container) {
    	console.log('$scope.openDetailsContainer')
    	console.log('1->')
    	console.log(server)
    	console.log('2->')
    	for (var firstKey in container) break;
    	console.log(firstKey)
        var compiledHtml = $compile(String(
            '<details_container container="getContainerByName(\'-s1-\',\'-c1-\')"' +
            'server="getServerByName(\'-s2-\')" ' +
            'callback-fn="updateData()" ' +
            '></details_container>')
                .replace("-s1-", server.servername)
                .replace("-s2-", server.servername)
                .replace("-s3-", JSON.stringify(server))
                //.replace("-c1-", container.name)
                .replace("-c1-", firstKey)
                .replace("-c2-", JSON.stringify(container))
        )($scope);
        $("#details_container").html(compiledHtml);
    },
    $scope.openDetailsServer = function(server) {
        var compiledHtml = $compile(String(
            '<details_server ' + 
            'server="getServerByName(\'-s1-\')" ' +
//            'serverinfo="getServerInfoByName(\'-s2-\')" ' +
            'containers="getContainersByServer(\'-s3-\')"' +
            '></details_server>')
                .replace("-s1-", server.servername)
//                .replace("-s2-", server.servername)
                .replace("-s3-", server.servername)
            )($scope);
//        console.log($scope.getServerInfoByName(server.servername));
        $("#details_container").html(compiledHtml);
    };
    
    // Socket experiment
    namespace = "/update";
    var socket = io.connect(
        "http://" 
        + document.domain 
        + ":" 
        + location.port 
        + namespace
    );

    socket.on("connect", function(msg) {
    	console.log("socket.on2");
        socket.emit(
            "connected", 
            {data: "Im connected!",}
        );
    });

    socket.on('disconnect', function(){
        console.log('user disconnected');
    });    
    
    socket.on('my_response', function(msg) {
    	console.log('response2');
    	$scope.updateData()
    });

    socket.on('destroy', function () {
    	console.log("Destroy");
        socket.removeListener('my_response');
    });    
 // Socket experiment
}]);


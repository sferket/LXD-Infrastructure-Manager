app.controller("MainController", ["$scope", "$http", "$compile", 
function($scope, $http, $compile) {
	
    $scope.servers = null,
    $scope.server = null,
    $scope.server_info = null,
    $scope.containers = null,
    $scope.container = null,
    
    $scope.selectedNode = null, 
    $scope.server_data = null,
    $scope.container_data = null,
    $scope.expandedNodes = {},
    $scope.checksumNodes = null,

    $scope.tmp = "/static/img/container-red.png" ;  //Experimenting
    
    // Get data from server when loading page
    $http({
        method: "GET",
        url: "/get_info"
    })
        .then(
            function Success(response) {
            	
         	
            	//console.log('ppppppppppppppppppppppppppppppppppppppp')
//                $scope.servers = response.data.servers;
//                $scope.server_info = response.data.server_info;
//                $scope.containers = response.data.containers;
//                //$scope.sections = response.data.sections;
//                
//                console.log("response: ", response);
//                console.log("servers: ", $scope.servers);
//                console.log("server_info: ", $scope.server_info);
//                console.log("containers: ", $scope.containers);
//                $scope.treeNodes =[{
//                	name: "Node 1",
//                	image: "/static/img/container-host.png",
//                        children: [{
//                            name: "test123",
//                            nodeID: "server.container.test123",
//                            //image: "/static/styles/img/virtual-machine-300px.png",
//                            image: "/static/img/container-green.png",
//                            children:[
//                				{name:"Node 1.1.1"},
//                				{name: "Node 1.1.2"}]
//                        }]
//                	},{
//                        name: "Node 2",
//                        children: [
//                			{name: "Node 2.1"},
//                			{name: "Node 2.2"}
//                		]
//                    }];
                
                $scope.treeNodes = response.data.tree ;
                $scope.checksumNodes = response.data.tree_checksum ;
                
                
//                $scope.treeNodes.push({
//                	name: "Node 100"
//                });
                
            },
            function Error(response) {
                console.log("Error getting data");
            }
        ),
        $scope.$on('selection-changed', function (e, node) {
            //node - selected node in tree
            $scope.selectedNode = node;
            $scope.server_data = null;
            $scope.container_data = null;
            
            //console.log(node);
            $scope.updateData()
            if (node.type == 'container') {
            	$scope.openDetailsContainer('', '');
            } else if (node.type == 'host') {
            	$scope.openDetailsServer('');
            }
            //node.disabled = true
            //node.image = "/static/img/container-red.png" ;
            //node.parentNode.removeChild(node);
            //$scope.treeNodes[0].expanded = false;
            //$scope.treeNodes[0] = null;
            //node.removeNode();
            
            $scope.treeNodes.push({name: "New Root", id:"some id", children: []})
            
            
        });
        $scope.$on('expanded-state-changed', function (e, node) {
            // node - the node on which the expanded state changed
            // to see the current state check the expanded property
            //console.log(node.expanded);
            //$scope.exapndedNode = node;  
        	if (node.expanded) {
        		$scope.expandedNodes[node.nodeId] = true;
        	} else {
        		delete $scope.expandedNodes[node.nodeId]
        	}
        });        
    $scope.updateData = function() {
//                $scope.treeNodes =[{
//                	name: "Node 1",
//                        children: [{
//                            name: "test123",
//                            nodeID: "server.container.test123",
//                            tst : "jjjj",
//                            children:[
//                				{name:"Node 1.1.1"},
//                				{name: "Node 1.1.2"}]
//                        }]
//                	},{
//                        name: "Node 200",
//                        children: [
//                			{name: "Node 2.1"},
//                			{name: "Node 2.2"}
//                		]
//                    }];   
        //$scope.server = new Date()
        $http({
            method: "GET",
            //url: "/get_info?tmp=".concat($scope.selectedNode.name),
            url: "/get_info",
            params : { 'host' : $scope.selectedNode.host, 'container' : $scope.selectedNode.container, 'checksumNodes' : $scope.checksumNodes}
        })
        .then(
            function Success(response) {
                $scope.server_data = response.data.server_data ;
                $scope.container_data = response.data.container_data ;

                if (response.data.tree){         // Check if checksum changed!!
                	console.log('-' + $scope.checksumNodes + '-');
                	$scope.checksumNodes = response.data.tree_checksum ;
                	$scope.treeNodes = response.data.tree ;

                	var loopNodes = function(arr) {
                		for (let n of arr){
                			if ($scope.expandedNodes[n.nodeId]){
                				n.expanded = true ;
                			}
            				
            				if (n.nodeId == $scope.selectedNode.nodeId) {
            					n.selected = true ;
            				}
            				
                			
                			if (n.children.length > 0){
                				loopNodes(n.children) ;
                			}
                		}
                		
                	}
                	loopNodes($scope.treeNodes);
                }
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
    	//console.log('=>')
//    	console.log($scope.servers[name])
        //return $scope.servers[name];
    	//var tmp = new Date().toString() ;
    	return $scope.server_data;
    },
//    $scope.getServerInfoByName = function(name) {
//        return $scope.server_info[name];
//    },
    $scope.getContainerByName = function(server, name) {
    	//console.log('===>', name )
//        var containers = $scope.getContainersByServer(server);
//    	var servers = $scope.servers
////    	console.log('1>', servers[server])
////    	console.log('2>', servers[server]['lxd_container_get'])
////    	console.log('3>', servers[server]['lxd_container_get']['test123'])
////    	console.log('3.1>', servers[server]['lxd_snapshots_all'])
//        for (c_index in servers[server]['lxd_container_get']){
////        	console.log('4>', c_index)
////        	console.log('4>', servers[server]['lxd_container_get'][c_index][name])
//        	
//            if (name in servers[server]['lxd_container_get'][c_index]) {
//            	ret = servers[server]['lxd_container_get'][c_index][name]; 
//            	//ret['snapshots'] = servers[server]['lxd_snapshots_all'][c_index][name];
//            	ret['snapshots'] = servers[server]['lxd_snapshots_all'][name]
//                return ret;
//            }
//        }
    	
    	return $scope.container_data ;
    	
//    	return servers[server]['lxd_container_get']['test123']
//        for (c_index in containers){ 
//            if (containers[c_index].name == name) {
//                return containers[c_index];
//            }
//        }
    },
    // Load detail directives on menu item click 
    $scope.openDetailsContainer = function(server, container) {
    	//console.log('$scope.openDetailsContainer')
    	//console.log('1->')
    	//console.log(server)
    	//console.log('2->')
    	//console.log(container)
    	for (var firstKey in container) break;
    	//console.log(firstKey)
        var compiledHtml = $compile(String(
            '<details_container container="getContainerByName(\'-s1-\',\'-c1-\')"' +
            'server="getServerByName(\'-s2-\')" ' +
            'callback-fn="updateData()" ' +
            '></details_container>')
                .replace("-s1-", server.servername)
                .replace("-s2-", server.servername)
                .replace("-s3-", JSON.stringify(server))
                .replace("-c1-", container.name)
                //.replace("-c1-", firstKey)
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
        var compiledHtml = $compile(String(
                '<details_server ' + 
                //'server="\'-s1-\'" ' +
                'server="getServerByName(\'-s1-\')" ' +
                '></details_server>')
//                    .replace("-s1-", $scope.ss)
                )($scope);
        //console.log(compiledHtml);
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


app.controller("MainController", ["$scope", "$http", "$compile", 
function($scope, $http, $compile) {
//    $scope.count = 10;
//    $scope.globalFunctions = function() {
//        $scope.count++;
//    };
    
    $scope.selectedNode = null, 
    $scope.server_data = null,
    $scope.container_data = null,
    $scope.expandedNodes = {},
    $scope.checksumNodes = null,
//    $scope.testFunc = function() {
//        console.log("Teststuff") ;
//    }
    // Get data from server when loading page
    $http({
        method: "GET",
        url: "/get_info"
    })
        .then(
            function Success(response) {
                $scope.treeNodes = response.data.tree ;
                $scope.checksumNodes = response.data.tree_checksum ;
            },
            function Error(response) {
                console.log("Error getting data");
            }
        ),
        $scope.$on('selection-changed', function (e, node) {
            $scope.selectedNode = node;
            $scope.server_data = null;
            $scope.container_data = null;
            
            $scope.updateData()
            if (node.type == 'container') {
            	console.log("openDetailsContainer");
            	$scope.openDetailsContainer('', '');
            } else if (node.type == 'host') {
            	console.log("openDetailsServer");
            	$scope.openDetailsServer('');
            } else {
            	console.log("node.type:" + node.type);
            	$scope.openDetailsMap();
            }
        });
        $scope.$on('expanded-state-changed', function (e, node) {
        	if (node.expanded) {
        		$scope.expandedNodes[node.nodeId] = true;
        	} else {
        		delete $scope.expandedNodes[node.nodeId]
        	}
        });   
        
    $scope.updateData = function() {
        $http({
            method: "GET",
            url: "/get_info",
            params : { 'host' : $scope.selectedNode.host, 'container' : $scope.selectedNode.container, 'checksumNodes' : $scope.checksumNodes}
        })
        .then(
            function Success(response) {
            	console.log('Scope update')
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
    $scope.getServerByName = function(name) {
    	return $scope.server_data;
    },
    $scope.getContainerByName = function(server, name) {
    	return $scope.container_data ;
    },
    $scope.getCount = function() {
    	return $scope.count ;
    },
    // Load detail directives on menu item click 
    $scope.openDetailsContainer = function(server, container) {
    	var compiledHtml = $compile(String(
		      '<details_container container="getContainerByName()"' +
		      'server="getServerByName()" ' +
		      'callback-fn="updateData()" ' +
		      '></details_container>')
		)($scope);
        
        $("#details").html(compiledHtml);
    },

    $scope.openDetailsServer = function(server) {
        var compiledHtml = $compile(String(
                '<details_server ' + 
                'server="getServerByName()" ' +
                '></details_server>')
                )($scope);
        $("#details").html(compiledHtml);
    };
    
    $scope.openDetailsMap = function() {
        var compiledHtml = $compile(String(
                '<details_map ' + 
                '></details_map>')
                )($scope);
        $("#details").html(compiledHtml);
    },
    
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
    
    socket.on('update', function(msg) {
    	console.log('response2');
    	$scope.updateData()
    });

    socket.on('destroy', function () {
    	console.log("Destroy");
        socket.removeListener('update');
    });    
 // Socket experiment
}]);


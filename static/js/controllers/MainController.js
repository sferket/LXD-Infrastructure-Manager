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
        console.log("updating")
        $http({
            method: "GET",
            url: "/get_info"
        })
        .then(
            function Success(response) {
                $scope.servers = response.data.servers;
                $scope.server_info = response.data.server_info;
                $scope.containers = response.data.containers;
                console.log("response: ", response);
                console.log("servers: ", $scope.servers);
                console.log("server_info: ", $scope.server_info);
                console.log("containers: ", $scope.containers);
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
        return $scope.servers[name];
    },
    $scope.getServerInfoByName = function(name) {
        return $scope.server_info[name];
    },
    $scope.getContainerByName = function(server, name) {
        var containers = $scope.getContainersByServer(server);
        for (c_index in containers){ 
            if (containers[c_index].name == name) {
                return containers[c_index];
            }
        }
    },
    // Load detail directives on menu item click 
    $scope.openDetailsContainer = function(server, container) {
        var compiledHtml = $compile(String(
            '<details_container container="getContainerByName(\'-s1-\',\'-c1-\')"' +
            'server="getServerByName(\'-s2-\')" ' +
            'callback-fn="updateData()" ' +
            '></details_container>')
                .replace("-s1-", server.servername)
                .replace("-s2-", server.servername)
                .replace("-s3-", JSON.stringify(server))
                .replace("-c1-", container.name)
                .replace("-c2-", JSON.stringify(container))
        )($scope);
        $("#details_container").html(compiledHtml);
    },
    $scope.openDetailsServer = function(server) {
        var compiledHtml = $compile(String(
            '<details_server ' + 
            'server="getServerByName(\'-s1-\')" ' +
            'serverinfo="getServerInfoByName(\'-s2-\')" ' +
            'containers="getContainersByServer(\'-s3-\')"' +
            '></details_server>')
                .replace("-s1-", server.servername)
                .replace("-s2-", server.servername)
                .replace("-s3-", server.servername)
            )($scope);
        console.log($scope.getServerInfoByName(server.servername));
        $("#details_container").html(compiledHtml);
    };
}]);

app.controller("MainController", ["$scope", "$http", "$compile", 
function($scope, $http, $compile) {
    $scope.servers = null,
    $scope.server = null,
    $scope.server_info = null,
    $scope.containers = null,
    $scope.container = null,
    $http({
        method: "GET",
        url: "/get_info"
    })
        .then(
            function Success(response) {
                console.log("response: ", response);
                $scope.servers = response.data.servers;
                console.log("servers: ", $scope.servers);
                $scope.server_info = response.data.server_info;
                console.log("server_info: ", $scope.server_info);
                $scope.containers = response.data.containers;
                console.log("containers: ", $scope.containers);
            },
            function Error(response) {
                console.log("Error getting data");
            }
        ),
    $scope.getContainersByServer = function(servername) {
        return $scope.containers[servername];
    },
    $scope.getServerByName = function(name) {
        return $scope.servers[name];
    },
    $scope.getContainerByName = function(server, name) {
        var containers = $scope.getContainersByServer(server);
        for (c_index in containers){ 
            if (containers[c_index].name == name) {
                return containers[c_index];
            }
        }
    },
    $scope.openDetailsContainer = function(server, container) {
        var compiledHtml = $compile(
            '<details_container container="getContainerByName(\'' +
            server.servername +
            '\',\'' +
            container.name +
            '\')"></details_container>')($scope);
        $("#details_container").html(compiledHtml);
    },
    $scope.openDetailsServer = function(server) {
        var compiledHtml = $compile(
            '<details_server server="getServerByName(\'' +
            server.servername +
            '\')"></details_server>')($scope);
        $("#details_container").html(compiledHtml);
    };
}]);

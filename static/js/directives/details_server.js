app.directive("detailsServer", ["$http", function($http) {
    return {
        restrict: "E",
        scope: {
            server: "=server",
            containers: "=containers"
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

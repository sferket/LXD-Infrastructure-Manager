app.directive("detailsContainer", ["$http", "$compile", function($http, $compile) {
    return {
        restrict: "E",
        scope: {
            container: "=container",
            server: "=server",
            up: "&callbackFn",
        },
        templateUrl: "/static/js/directives/details_container.html",
        link: function($scope, element, attrs) {
            $scope.runContainerMethod = function(server, container, method, type, snap) {
                console.log("runcontainermethod");
                var data = {
                    "server": server,
                    "container": container,
                    "method": method,
                    "type": type,
                    "snap": snap
                };
                data = JSON.stringify(data);
                var config = {
                    headers: {
                        "Content-Type": "application/json",
                    }
                }
                $http.post("/container_cmd/", data, config)
                    .success(function (data, status, headers, config) {
                        $scope.up({});
                    })
                    .error(function (data, status, header, config) {
                        console.log("error");
                    });
            };
        }
    }
}]);

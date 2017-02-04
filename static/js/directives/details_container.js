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
                //console.log("Element: ", element);
                //console.log("Type: " , typeof(element));
                //console.log("j: ", element.find("#tar_name"));
                //console.log("2: ", element.find("#tar_name").val());
                // element["0"].childNodes["0"].childNodes[1].childNodes[1]
                // .childNodes[3].childNodes[1].childNoes[3].value;
                var data = {
                    "server": server,
                    "container": container,
                    "method": method,
                    "type": type,
                    "snap": snap,
                    "tar_name": element.find("#tar_name").val(),
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

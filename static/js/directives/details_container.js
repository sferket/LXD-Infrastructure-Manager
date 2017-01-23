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
                    "snap": snap,
                    "tar_snap": element.find("#tar_snap").val(),
                    "tar_cont": element.find("#tar_cont").val(),
                    "tar_prof": ""
                };
                try {
                    var profile_element = element.find("#tar_prof")["0"];
                    var option_index = profile_element.selectedIndex;
                    var option_value = profile_element[option_index].text;
                    data["tar_prof"] = option_value 
                    console.log("aa ", option_value);
                    console.log("bb ", data["tar_prof"]);
                } catch (err) { console.log("target profile not found"); }

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
            },
            $scope.update_tar_cont = function(s) {
                element.find("#tar_cont").attr('placeholder', s)
            }
        }
    }
}]);

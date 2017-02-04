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
                console.log(snap);
                console.log(element.find("#tar_name").val());

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
                    	console.log("Success!!!!");
                    	console.log(data);
                    	//data.architecture = 'Stefaan' ;
                    	//container.architecture = 'TTTT' ;
                    	console.log(data);
                    	console.log(status);
                    	console.log(headers);
                    	console.log(config);
                        $scope.up({});
                    })
                    .error(function (data, status, header, config) {
                        console.log("error");
                    });
            };
         
            $scope.update_tar_cont = function(s) {
            	//element.find("#tar_cont").attr('placeholder', s)
            	console.log(s);
            	console.log(new Date().toISOString().substring(0, 10).replace(/-/g,''))
            	console.log(new Date().toISOString().substring(11, 19))
            	dat = new Date().toISOString();
            	document.getElementById('tar_name').value = dat.substring(0, 10).replace(/-/g,'') + dat.substring(11, 19).replace(/:/g,'');
            	//document.getElementById('snapname').value = 'test123';
            }            
/*            $scope.getDefaultName = function(server, container) {
                console.log("getDefaultName");
                //console.log("Element: ", element);
                //console.log("Type: " , typeof(element));
                //console.log("j: ", element.find("#tar_name"));
                //console.log("2: ", element.find("#tar_name").val());
                // element["0"].childNodes["0"].childNodes[1].childNodes[1]
                // .childNodes[3].childNodes[1].childNoes[3].value;
                var data = {
                    "server": server,
                    "container": container,
                };
                data = JSON.stringify(data);
                var config = {
                    headers: {
                        "Content-Type": "application/json",
                    }
                }
                $http.post("/get_default_name_r/", data, config)
                    .success(function (data, status, headers, config) {
                    	console.log("Success!!!!");
                    	console.log(data);
                        $scope.up({});
                    })
                    .error(function (data, status, header, config) {
                        console.log("error");
                    });
            };            
*/        }
    }
}]);

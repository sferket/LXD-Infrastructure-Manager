app.directive("menuServers", function() {
    return {
        restrict: "E",
        transclude: true,
        scope: {
            server: "=server",
            serverClick: "&",
            myStyle: "=myStyle",
        },
        templateUrl: "/static/js/directives/menu_servers.html",
        controller: function($scope) {
            this.addItem = function(val) {
                console.log(val);
            }
        },
        link: function($scope, elem, attrs) {
            $scope.toggle = true;
        }
    }
});

app.directive("menuContainers", function() {
    return {
        restrict: "E",
        require: "^menu-servers",
        scope: {
            container: "=container",
        },
        templateUrl: "/static/js/directives/menu_containers.html",
        link: function(scope, elem, attr, outercontrol) {
            outercontrol.addItem(1);
        }
    }
});

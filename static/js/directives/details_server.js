app.directive("detailsServer", function() {
    return {
        restrict: "E",
        scope: {
            server: "=server",
        },
        templateUrl: "/static/js/directives/details_server.html",
    }
});

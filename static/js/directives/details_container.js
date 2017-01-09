app.directive("detailsContainer", function() {
    return {
        restrict: "E",
        scope: {
            container: "=container",
        },
        templateUrl: "/static/js/directives/details_container.html",
    }
});

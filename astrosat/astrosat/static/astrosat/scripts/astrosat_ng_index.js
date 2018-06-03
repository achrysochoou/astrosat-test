/* ng_index.js */
/* ng app for dealing w/ the index page */


(function() {

    var app = angular.module('FacilitiesApp',[]);

    app.config(['$httpProvider', '$provide', function($httpProvider, $provide) {
        /* NG serializes data as pure JSON, while Django expects form parameters w/ CSRF protection*/
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);

    app.controller('FacilitiesController', [ "$http", "$q", function($http, $q) {

        var facilities_controller = this;

        var _blocking = false;
        var _loaded = false;

        var _api_facilities_url = "/api/facilities/";
        var _api_tasks_url = "/api/tasks/";
        var _service_import_url = "/services/import_facilities/"

        facilities_controller.is_admin = is_admin;

        facilities_controller.facilities = [];
        facilities_controller.tasks = [];

        facilities_controller.load = function() {
            var deferred = $q.defer();
            var asynch_calls = [
                $http.get(_api_facilities_url),
                $http.get(_api_tasks_url)
            ];
            facilities_controller._blocking = true;
            $q.all(asynch_calls).then(
                function(responses) {
                    facilities_controller.facilities = responses[0].data;
                    facilities_controller.tasks = responses[1].data;
                    facilities_controller._blocking = false;
                },
                function(responses) {
                    deferred.reject(responses)
                    console.log(responses)
                    show_msg("Error loading data.", "error")
                    facilities_controller._blocking = false;
                }
            )
            return deferred.promise;
        }

        facilities_controller.import_facilities = function() {
            facilities_controller._blocking = true;
            $http({
                method: "POST",
                url: _service_import_url,
            }).then(
                /* success block */
                function(response) {
                    facilities_controller.load();
                },
                /* error block */
                function(response) {
                    console.log(response.data);
                    show_msg("Error importing facilities.", "error");
                }
            ).finally(function() {
                facilities_controller._blocking = false;
            });
        }

        facilities_controller.disable_event = function(e, disable) {
            /* enable or disable an event */
            if (disable == true) {
                e.preventDefault();
            }
        }

        facilities_controller.blocking = function() {
            return facilities_controller._blocking;
        }

        facilities_controller.load()

    }]);

 })();

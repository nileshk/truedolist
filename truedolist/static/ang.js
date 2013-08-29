/* -*-mode:js; js-indent-level: 2 -*- */

angular.module('todoServices', ['ngResource']).
  factory('TodoLists', function($resource) {
    return $resource('/api/lists', {}, {
      query: { method: 'GET', isArray: true }
    });
  }).
  factory('TodoLabels', function($resource) {
    return $resource('/api/labels', {}, {
      query: { method: 'GET', isArray: true }
    });
  }).
  factory('TodoListItems', function($resource) {
    return $resource('/api/lists/:listId/items/', {listId:'@id'}, {
      query: { method: 'GET', isArray: true }
    });
  });

angular.module('trueDoList', ['ngRoute', 'todoServices']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.
      when('/lists/:listId', { templateUrl: 'list-detail.html', controller: ListController}).
      otherwise({redirectTo: '/'});
  }]);


function TodoListController($scope, TodoLists, TodoLabels) {
  $scope.lists = TodoLists.query();
  $scope.labels = TodoLabels.query();
}

function ListController($scope, $routeParams, TodoListItems) {
  var listId = $routeParams.listId;
  $scope.items = TodoListItems.query({listId: listId});
}
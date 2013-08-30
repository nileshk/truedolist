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
    return $resource('/api/lists/:listId/items/', {listId:'@listId'}, {
      query: { method: 'GET', isArray: true },
      add: { method:'POST' },
    });
  }).

angular.module('trueDoList', ['ngRoute', 'todoServices']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.
      when('/lists/:listId', { templateUrl: 'list-detail.html', controller: ListController}).
      otherwise({redirectTo: '/'});
  }]);


function TodoListController($scope, TodoLists, TodoLabels, TodoListItems) {
  $scope.lists = TodoLists.query();
  $scope.labels = TodoLabels.query();

  $scope.addItem = function() {
    if ($scope.itemEditInput === "" || $scope.listId === undefined) {
      return false;
    }
    alert('adding ' + $scope.itemEditInput + ':' + $scope.listId);
    var newItem = new TodoListItems();
    newItem.listId = $scope.listId;
    newItem.title = $scope.itemEditInput;
    newItem.$add();
    // TODO reload list
    // TODO animate new item
  };

  $scope.selectList = function(listId) {
    $scope.listId = listId;
  };
}

function ListController($scope, $routeParams, TodoListItems) {
  var listId = $routeParams.listId;
  $scope.listId = $routeParams.listId;
  $scope.items = TodoListItems.query({listId: listId});
}

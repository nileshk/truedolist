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
  factory('TodoItem', function($resource) {
    return $resource('/api/items/:itemId/', {itemId:'@itemId'}, {
      save: { method:'POST', params: {request_method: 'PUT' } }
    });
  });

  
angular.module('trueDoList', ['ngRoute', 'ngAnimate', 'todoServices']);
/*
.
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.
      when('/lists/:listId', { templateUrl: 'list-detail.html', controller: ListController}).
      otherwise({redirectTo: '/'});
  }]);
*/

function TodoListController($scope, TodoLists, TodoLabels, TodoListItems, TodoItem) {
  $scope.lists = TodoLists.query();
  $scope.labels = TodoLabels.query();

  $scope.addItem = function() {
    if ($scope.itemEditInput === "" || $scope.listId === undefined) {
      return false;
    }
    var newItem = new TodoListItems();
    newItem.listId = $scope.listId;
    newItem.title = $scope.itemEditInput;
    newItem.$add(function() {
      $scope.selectList($scope.listId);
    });
  };

  $scope.saveItem = function() {
    if ($scope.itemEditInput === "" || $scope.editItemId === undefined) {
      return false;
    }
    var itemToSave = new TodoItem();
    itemToSave.itemId = $scope.editItemId;
    itemToSave.title = $scope.itemEditInput;
    itemToSave.$save(function() {
      $scope.selectList($scope.listId, $scope.listTitle);
    });

  };

  $scope.deleteItem = function(itemId) {
    if (confirm('Delete item?')) {
      TodoItem.delete({itemId: itemId}, function() {
        // TODO animate item removal
        $scope.selectList($scope.listId, $scope.listTitle);
      });
    }
  }
  
  $scope.selectList = function(listId, listTitle) {
    // TODO: Just take list as parameter
    $scope.listId = listId;
    $scope.listTitle = listTitle;
    $scope.listItems = TodoListItems.query({listId: listId});
  };

  $scope.beginEdit = function(itemId, title) {
    $scope.editItemId = itemId;
    $scope.itemEditInput = title;
  };

  $scope.cancelAction = function() {
    $scope.editItemId = null;
    $scope.itemEditInput = '';
  };
}

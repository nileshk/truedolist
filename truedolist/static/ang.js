/* -*-mode:js; js-indent-level: 2 -*- */

angular.module('todoServices', ['ngResource']).
  factory('TodoLists', function($resource) {
    return $resource('/api/lists/:action/:listId/', {listId:'@listId'}, {
      query: { method: 'GET', isArray: true },
      reposition: { method:'POST', params: { action: 'reposition' } }
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
      add: { method:'POST' }
    });
  }).
  factory('TodoItem', function($resource) {
    return $resource('/api/items/:action/:itemId/', {itemId:'@itemId'}, {
      save: { method:'POST', params: { request_method: 'PUT' } },
      move: { method:'POST', params: { action: 'move' } },
      reposition: { method:'POST', params: { action: 'reposition' } },
      highlight: { method:'POST', params: { action: 'highlight' } }
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

function TodoListController($scope, TodoLists, TodoLabels, TodoListItems, 
                            TodoItem) {
  $scope.lists = TodoLists.query();
  $scope.labels = TodoLabels.query();

  $scope.refreshLists = function() {
    $scope.lists = TodoLists.query();
  }
  
  $scope.editSubmit = function() {
    if ($scope.editItemId) {
      $scope.saveItem();
    } else {
      $scope.addItem();
    }
  }
  
  $scope.addItem = function() {
    if ($scope.itemEditInput === "" || $scope.listId === undefined) {
      return false;
    }
    var newItem = new TodoListItems();
    newItem.listId = $scope.listId;
    newItem.title = $scope.itemEditInput;
    newItem.$add(function() {
      $scope.itemEditInput = '';
      $scope.refreshCurrentList();
    });
  }

  $scope.saveItem = function() {
    if ($scope.itemEditInput === "" || $scope.editItemId === undefined) {
      return false;
    }
    var itemToSave = new TodoItem();
    itemToSave.itemId = $scope.editItemId;
    itemToSave.title = $scope.itemEditInput;
    itemToSave.$save(function() {
      $scope.refreshCurrentList();
    });
  }

  $scope.createList = function() {
    var title = prompt("Enter title of new list", "");
    if (title !== null) {
      var listToSave = new TodoLists();
      listToSave.title = title;
      listToSave.$save(function(savedList) {
        $scope.selectList(savedList.id, title);
        $scope.refreshLists();
      });
    }
  }

  $scope.deleteItem = function(itemId) {
    if (confirm('Delete item?')) {
      TodoItem.delete({itemId: itemId}, function() {
        // TODO animate item removal
        $scope.refreshCurrentList();
      });
    }
  }

  $scope.deleteList = function(listId) {
    if (confirm('Delete list?')) {
      TodoLists.delete({listId: listId}, function() {
        // TODO animate list removal
        $scope.listId = null;
        $scope.listTitle = null;
        $scope.listItems = null;
        $scope.cancelAction();
        $scope.refreshLists();
      });
    }
  }

  $scope.highlightItem = function(itemId, highlightColor) {
    var parameters = { p:'p' } // TODO Need at least one param or get 404
    parameters.itemId = itemId;
    parameters.highlight_color = highlightColor;

    TodoItem.highlight(parameters, function() {
      // TODO animation
      $scope.refreshCurrentList();
    });
  }
  
  $scope.refreshCurrentList = function() {
    $scope.selectList($scope.listId, $scope.listTitle);
  }
  
  $scope.selectList = function(listId, listTitle) {
    // TODO: Just take list as parameter
    $scope.listId = listId;
    $scope.listTitle = listTitle;
    $scope.listItems = TodoListItems.query({listId: listId});
  }

  $scope.listClick = function(listId, listTitle) {
    if ($scope.moveListId) {
      TodoLists.reposition(
        { listId: $scope.moveListId, before_id: listId },
        function() {
          $scope.cancelAction();
          $scope.refreshLists();
        });
    } else if ($scope.moveItemId) {
      TodoItem.move(
        { itemId: $scope.moveItemId, destination_list_id: listId },
        function() {
          $scope.cancelAction();
          $scope.refreshCurrentList();
        });
    } else {
      $scope.selectList(listId, listTitle);
    }
  }
  
  $scope.itemClick = function(item) {
    if ($scope.moveItemId) {
      TodoItem.reposition(
        { itemId: $scope.moveItemId, before_id: item.id },
        function() {
          $scope.cancelAction();
          $scope.refreshCurrentList();
        });
    }
  }

  $scope.startMove = function(item) {
    $scope.moveItemId = item.id;

    $scope.statusMessageAreaClass = 'notice';
    $scope.statusMessageAreaHeading = 'Moving Todo Item:';
    $scope.statusMessageAreaMessage = 'Click on list to move to ' +
      'or place in list of todo items to move to';
  }

  $scope.startMoveList = function(listId) {
    $scope.moveListId = listId;

    $scope.statusMessageAreaClass = 'notice';
    $scope.statusMessageAreaHeading = 'Moving Todo List:';
    $scope.statusMessageAreaMessage = 'Click on place in list of todo lists to move to';
  }
  
  $scope.beginEdit = function(itemId, title) {
    $scope.editItemId = itemId;
    $scope.itemEditInput = title;
  }

  $scope.beginEditList = function(listId, listTitle) {
    $scope.editListId = listId;
    $scope.itemEditInput = listTitle;
  }
  
  $scope.cancelAction = function() {
    $scope.editItemId = null;
    $scope.itemEditInput = '';
    $scope.moveItemId = null;
    $scope.moveListId = null;
    $scope.editListId = null;
    $scope.itemEditInput = null;

    $scope.statusMessageAreaClass = null;
    $scope.statusMessageAreaHeading = null;
    $scope.statusMessageAreaMessage = null;

    $scope.showOptions = false;
    $scope.showListOptions = false;
  }
}

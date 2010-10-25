/* -*-mode:js; js-indent-level: 2 -*- */
//(function(){

var FX_TRANSFER_DELAY = 350;
var FX_HIGHLIGHT_DELAY = 1000;
var FX_SLIDE_DELAY = 500;

var current_list_id = null;
var current_list_title = null;
var current_item_id = null;
var current_item_title = null;
var is_moving_item = false;
var is_moving_list = false;
var is_item_edit_mode = false;
var is_list_edit_mode = false;
var is_labelling_list = false;
var lists = null;
var labels = null;

function loadLists(callback) {
  $("#lists").empty();
  $.getJSON('/api/lists/',
    function(results) {
      lists = new Array();
      $.each(results, function(i, item) {
        lists[item.id] = { title: item.title };
        $('<li><div id="todoList' + item.id +
          '" class="todoList" /></li>').appendTo("#lists");
        $("#todoList" + item.id).text(item.title);
        $("#todoList" + item.id).click(
          function() {
            //loadItemsForList(item.id);
            selectTodoList(item.id, item.title);
          });
      });
      if (callback !== undefined && callback !== null) {
        callback();
      }
    });
}

function loadItemsForList(list_id, callback) {
  $.getJSON("/api/lists/" + list_id + "/items/",
    function( results ) {
      $("#items").empty();
      $('<h2 id="listTitle" class="alt" />' +
        '<div id="listOptions"></div><ul>').appendTo("#items");
      $("#listTitle").text(current_list_title);
      $("#listTitle").click(showTodoListOptions);
      $.each(results,
        function(i, item) {
          $('<li><div id="' + getTodoItemId(item.id) +
            '">' + item.title + '</div></li>').appendTo("#items");
          $("#todoItem" + item.id).text(item.title);
          $("#todoItem" + item.id).click(function() {
                                           selectTodoItem(item.id, item.title);
                                         });
          if (item.highlight_color !== null) {
            $("#todoItem" + item.id).addClass('ui-state-highlight');
          }
        });
      $('</ul>').appendTo("#items");
      if (callback !== undefined && callback !== null) {
        callback();
      }
    });
}

function loadLabels(callback) {
  $("#labels").empty();
  $.getJSON('/api/labels/',
    function(results) {
      labels = new Array();
      $.each(results, function(i, item) {
        labels[item.id] = { title: item.title };
        $('<li><div id="todoLabel' + item.id +
          '" class="todoLabel" /><div id="todoLabel' + item.id +
          'Lists" /></li>').appendTo("#labels");
        $("#todoLabel" + item.id).text(item.title);
        $("#todoLabel" + item.id).click(
          function() {
            selectTodoLabel(item.id);
          });
      });
      if (callback !== undefined && callback !== null) {
        callback();
      }
    });
}

function getTodoItemId(todo_item_id) {
  return "todoItem" + todo_item_id;
}

function getTodoItem(todo_item_id) {
  return $("#" + getTodoItemId(todo_item_id));
}

function getTodoListId(todo_list_id) {
  return "todoList" + todo_list_id;
}

function getTodoList(todo_list_id) {
  return $("#" + getTodoListId(todo_list_id));
}

function getTodoLabelId(todo_label_id) {
  return "todoLabel" + todo_label_id;
}

function getTodoLabel(todo_label_id) {
  return $("#" + getTodoLabelId(todo_label_id));
}

function getNumberFromTodoListId(todo_list_id) {
  return todo_list_id.substring(8);
}

function focusInput() {
  $("#itemEditInput").focus();
}

function selectNoList() {
  $("#items").empty();
}

function selectTodoList( list_id, list_title ) {
  if (list_title === undefined || list_title === null) {
    list_title = lists[list_id].title;
  }
  if (is_moving_item) {
    moveItemToList(list_id);
    return;
  }
  if (is_moving_list) {
    repositionList(list_id);
    return;
  }
  current_list_id = list_id;
  current_list_title = list_title;
  loadItemsForList(list_id);
}

function showTodoListOptions() {
  todoItemModeNew();
  $("#listOptions").empty();
  $("#listOptions").append(
    '<a id="todoListOptionEdit" href="#">Edit</a> ' +
    '<a id="todoListOptionDelete" href="#">Delete</a> ' +
    '<a id="todoListOptionMove" href="#">Move</a> ' +
    '<a id="todoListOptionLabel" href="#">Label</a> ' +
    '<a id="todoListOptionCancel" href="#">Cancel</a>'
  );
  $("#todoListOptionEdit").click(todoListModeEdit);
  $("#todoListOptionDelete").click(deleteList);
  $("#todoListOptionMove").click(moveList);
  $("#todoListOptionLabel").click(labelList);
  $("#todoListOptionCancel").click(todoItemModeNew);
}

function todoListModeEdit() {
  is_list_edit_mode = true;
  $("#itemEditInput").val(current_list_title);
  $("#itemEditButtons").empty();
  $('<input value="Save list" ' +
    'class="button" type="submit" id="saveTodoList" />' +
    '<input value="Cancel" class="button" type="submit" ' +
    'id="cancelEditTodoList" />').appendTo("#itemEditButtons");
  $("#saveTodoList").click(renameList);
  $("#cancelEditTodoList").click(todoItemModeNew);
  focusInput();
}


function todoListOptionsCancel() {
  is_moving_list = false;
  is_labelling_list = false;
  $("#listOptions").empty();
}

function selectTodoItem( item_id, item_title ) {
  if (is_moving_item) {
    repositionItem(item_id);
    return;
  }
  if (is_moving_list) {
    // Cancelling move list
    moveList();
  }
  todoItemModeNew();
  current_item_id = item_id;
  current_item_title = item_title;
  $("#renameItemTitle").val(item_title);
  $("#todoItemOptions").remove();
  //$("#listOptions").empty();
  $("#todoItem" + item_id).after('<div id="todoItemOptions">' +
    '<a id="todoItemOptionEdit" class="button" href="#">Edit</a> ' +
    '<a id="todoItemOptionDelete" class="button" href="#">Delete</a> ' +
    '<a id="todoItemOptionMove" class="button" href="#">Move</a> ' +
    '<a id="todoItemOptionCancel" class="button" href="#">Cancel</a> ' +
    '<a id="todoItemOptionHighlight" class="button" href="#">Highlight</a> ' +
    '<a id="todoItemOptionUnhighlight" class="button" href="#">Unhighlight</a> ' +
    '</div>');
  $("#todoItemOptionEdit").click(todoItemModeEdit);
  $("#todoItemOptionDelete").click(deleteItem);
  $("#todoItemOptionMove").click(moveItem);
  $("#todoItemOptionCancel").click(todoItemModeNew);
  $("#todoItemOptionHighlight").click(function() { 
    highlightItem(current_item_id, 1);
  });
  $("#todoItemOptionUnhighlight").click(function() { 
    highlightItem(current_item_id, null);
  });
}

function todoItemModeEdit() {
  is_item_edit_mode = true;
  $("#itemEditInput").val(current_item_title);
  $("#itemEditButtons").empty();
  $('<input value="Save item" ' +
    'class="button" type="submit" id="saveTodoItem" />' +
    '<input value="Cancel" class="button" type="submit" ' +
    'id="cancelEditTodoItem" />').appendTo("#itemEditButtons");
  $("#saveTodoItem").click(renameItem);
  $("#cancelEditTodoItem").click(todoItemModeNew);
  focusInput();
}

function todoItemModeNew() {
  is_item_edit_mode = false;
  is_list_edit_mode = false;
  $("#itemEditInput").val("");
  $("#itemEditButtons").empty();
  $('<input value="+ New item" ' +
    'class="button" type="submit" ' +
    'id="saveNewTodoItem" />').appendTo("#itemEditButtons");
  $("#saveNewTodoItem").click(addItem);
  todoItemOptionsCancel();
  todoListOptionsCancel();
  clearStatusMessage();
  focusInput();
  return false;
}

function todoItemOptionsCancel() {
  is_moving_item = false;
  $("#todoItemOptions").remove();
  current_item_id = null;
}

function addItem() {
  var title = $("#itemEditInput").val();
  var parameters = { title: title, request_method: "PUT" };
  $.post("/api/lists/" + current_list_id + "/items/", parameters,
         function ( result, textStatus ) {
           loadItemsForList(current_list_id,
             function() {
               highlight($("#items > *:last"));
             });
           $("#itemEditInput").val("");
           return false;
         }, "json");
  return false; // Cancel form POST
}

function newListDialog() {
  var newTitle = prompt("Enter title of new list", "");
  if (newTitle !== null) {
    addList(newTitle);
    // TODO Switch to list after creation
  }
}

function addList(title) {
  if (title === null || title === undefined) { // XXX Is this correct?
    title = $("#addListTitle").val();
  }
  var parameters = { title: title, request_method: "PUT" };
  $.post("/api/lists/", parameters,
         function ( result, textStatus ) {
           loadLists(
             function() {
               selectTodoList(getNumberFromTodoListId(
                                $("#lists> li > *:last").attr("id")));
               focusInput();
             }
           );
           return false;
         }, "json");
  return false; // Cancel form POST
}

function renameList() {
  var title = $("#itemEditInput").val();
  var parameters = { title: title, request_method: "PUT" };
  var rename_list_id = current_list_id;
  $.post("/api/lists/" + rename_list_id + "/", parameters,
         function ( result, textStatus ) {
           // TODO check for error condition
           loadLists();
           loadItemsForList(rename_list_id,
             function() {
               highlight(getTodoList(rename_list_id));
               highlight($("#listTitle"));
             });
           current_list_title = title;
           $("#itemEditInput").val("");
           return false;
         }, "json");
  return false; // Cancel form POST
}

function renameItem() {
  var title = $("#itemEditInput").val();
  var parameters = { title: title, request_method: "PUT" };
  var rename_item_id = current_item_id;
  $.post("/api/items/" + rename_item_id + "/", parameters,
         function ( result, textStatus ) {
           // TODO check for error condition
           loadItemsForList(current_list_id,
             function() {
               highlight(getTodoItem(rename_item_id));
             });
           todoItemModeNew();
           return false;
         }, "json");
  return false; // Cancel form POST
}

function deleteList() {
  if (confirm("Delete list and all the items it contains?")) {
    var parameters = { request_method: "DELETE" };
    $.post("/api/lists/" + current_list_id + "/", parameters,
           function ( result, textStatus ) {
             // TODO handle failures
             $("#items").hide("slide", { direction: "right" }, FX_SLIDE_DELAY,
               function() {
                 loadLists();
                 todoItemModeNew();
                 selectNoList();
                 $("#items").show();
               });
             return false;
           }, "json");
  }
  return false; // Cancel form POST
}

function deleteItem() {
  if (confirm("Delete item?")) {
    var parameters = { request_method: "DELETE" };
    $.post("/api/items/" + current_item_id + "/", parameters,
           function ( result, textStatus ) {
             // TODO handle failures
             getTodoItem(current_item_id).hide("slide",
               { direction: "right" }, FX_SLIDE_DELAY,
               function() {
                 loadItemsForList(current_list_id);
                 todoItemModeNew();
               });
             return false;
           }, "json");
  }
  return false; // Cancel form POST
}

function moveItem() {
  is_moving_item = !is_moving_item;
  if (is_moving_item) {
    displayStatusMessage('<span class="loud">Moving Todo Item:</span> ' +
                         'Click on list to move to ' +
                         'or place in list of todo items to move to', "notice");
    if (is_moving_list) {
      moveList();
    }
  } else {
    clearStatusMessage();
  }
}

function moveList() {
  is_moving_list = !is_moving_list;
  if (is_moving_list) {
    displayStatusMessage('<span class="loud">Moving Todo List:</span> Click '
                         + 'on place in list of todo lists to move to',
                         "notice");
    $("#moveListButton").text("Cancel Move List");
    if (is_moving_item) {
      moveItem();
    }
  } else {
    clearStatusMessage();
  }
}

function labelList() {
  is_labelling_list = !is_labelling_list;
  if (is_labelling_list) {
    displayStatusMessage('<span class="loud">Labelling Todo List:</span> Click '
                         + 'on label to apply to this todo list',
                         "notice");
    $("#todoListOptionLabel").text("Cancel Label");
  } else {
    clearStatusMessage();
    $("#todoListOptionLabel").text("Label");
  }
}

function moveItemToList( list_id ) {
  if (is_moving_item && current_item_id !== null) {
    var parameters = { destination_list_id: list_id };
    $.post("/api/items/move/" + current_item_id + "/", parameters,
           function ( result, textStatus ) {
             getTodoItem(current_item_id).effect("transfer",
               { to: "#" + getTodoListId(list_id) }, FX_TRANSFER_DELAY,
               function() {
                 loadItemsForList(current_list_id,
                   function() {
                     bounce(getTodoList(list_id));
                     //highlight(getTodoList(list_id));
                   }
                 );
               });
             return false;
           }, "json");
    moveItem();
  }
  return false; // Cancel form POST
}

function repositionList( list_id ) {
  if (is_moving_list && current_list_id !== null) {
    var parameters = { before_id: list_id };
    var moving_list_id = current_list_id;
    $.post("/api/lists/reposition/" + moving_list_id + "/", parameters,
           function ( result, textStatus ) {
             getTodoList(moving_list_id).effect("transfer",
               { to: "#" + getTodoListId(list_id) }, FX_TRANSFER_DELAY,
               function() {
                 loadLists(
                   function() {
                     bounce(getTodoList(moving_list_id));
                   }
                 );
               });
             return false;
           }, "json");
    moveList();
  }
  return false; // Cancel form POST
}

function repositionItem( item_id ) {
  if (is_moving_item && current_item_id !== null) {
    var parameters = { before_id: item_id };
    var moving_item_id = current_item_id;
    $.post("/api/items/reposition/" + current_item_id + "/", parameters,
           function ( result, textStatus ) {
             getTodoItem(moving_item_id).effect("transfer",
               { to: "#" + getTodoItemId(item_id) }, FX_TRANSFER_DELAY,
               function() {
                 loadItemsForList(current_list_id,
                   function() {
                     bounce(getTodoItem(moving_item_id));
                     });
               });
             return false;
           }, "json");
    moveItem();
  }
  return false; // Cancel form POST
}

function highlightItem( item_id, highlight_color ) {
  if (item_id !== null) {
    var parameters = { p:'p' } // TODO Need at least one param or get 404
    if (highlight_color !== null) {
      parameters.highlight_color = highlight_color
    }
    $.post("/api/items/highlight/" + item_id + "/", parameters,
           function ( result, textStatus ) {
             loadItemsForList(current_list_id,
                              function() {
                                bounce(getTodoItem(item_id));
                              });
             return false;
           }, "json");
  }
  return false; // Cancel form POST
}
    
function newLabelDialog() {
  var newTitle = prompt("Enter title of new label", "");
  if (newTitle !== null) {
    addLabel(newTitle);
    // TODO Switch to label after creation
  }
}

function addLabel(title) {
  if (title === null || title === undefined) { // XXX Is this correct?
    title = $("#addLabelTitle").val();
  }
  var parameters = { title: title, request_method: "PUT" };
  $.post("/api/labels/", parameters,
         function ( result, textStatus ) {
           loadLabels(
             function() {
//               selectTodoLabel(getNumberFromTodoLabelId(
//                                $("#labels> li > *:last").attr("id")));
               focusInput();
             }
           );
           return false;
         }, "json");
  return false; // Cancel form POST
}

function selectTodoLabel(label_id, callback) {
  var label_node = $("#todoLabel" + label_id + "Lists");
  var todo_label = $("#todoLabel" + label_id + "Lists > ul");
  if (is_labelling_list) {
    addLabelToSelectedList(label_id);
    return;
  }
  
  if (todo_label !== null && todo_label.length > 0) {
    // Collapse label lists
    todo_label.remove();
    if (callback !== undefined && callback !== null) {
      callback();
    }
    return;
  }
  // Expand label lists
  $.getJSON('/api/labels/' + label_id + '/lists/',
    function(results) {
      label_node.append("<ul/>");
      $.each(results, function(i, item) {
//        labels[item.id] = { title: item.title };
        var div_id = 'label' + label_id + 'todoList' + item.id;
        $("#todoLabel" + label_id + 'Lists > ul').append('<li><div id="' +
          div_id + '" class="todoList" /></li>');
        $("#" + div_id).text(item.title);
        $("#" + div_id).click(
          function() {
            selectTodoList(item.id);
          });
      });
      if (callback !== undefined && callback !== null) {
        callback();
      }
    });

}

function addLabelToSelectedList(label_id) {
  if(is_labelling_list && current_list_id !== null) {
    var parameters = { p: 'p' }; // Have to post something
    // /api/lists/:list_id/labels/:label_id/
    $.post("/api/lists/" + current_list_id + "/labels/" +
           label_id + "/", parameters, 
           function(results, textStatus) {
             loadLabels(function() {
               bounce(getTodoLabel(label_id));
               labelList(); // Cancel labelling
             });
           });
  }
}


function displayStatusMessage(message, status) {
  $("#statusMessageArea").empty();
  $("#statusMessageArea").append('<div class="' + status + '">' +
                                 message + '</div>');
}

function clearStatusMessage() {
  $("#statusMessageArea").empty();
}

function highlight(jqueryObject) {
  jqueryObject.effect("highlight", {}, FX_HIGHLIGHT_DELAY);
}

function bounce(jqueryObject) {
  jqueryObject.effect("bounce", { times:2 }, 300);
}

$(document).ready(
  function() {
    $("#sidebarTabs").tabs();
    loadLists();
    loadLabels();
    $("#newListButton").click(newListDialog);
    $("#newLabelButton").click(newLabelDialog);
    todoItemModeNew();
  });

//})();

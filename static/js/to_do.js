// this function is called when the checkbox icon is clicked
function toggleTaskComplete(e) {
    
    // this just gets the other cells in the row
    var cells = $(e.target).parent().parent().children();
    
    var task = {
	id: parseInt($(cells[0]).text()), // get the id, and parse it to an integer
	title: $(cells[1]).text(), // get the title
	description: $(cells[2]).text(),
	done: $(e.target).hasClass("fa-square-o") ? true : false // checks if its checked, or unchecked
    }
    
    // send the task to the server
    $.ajax({
	url: "/todo/api/update_task/" + task["id"],
	method: "POST",
	data: task,
	dataType: "json",
	context: e.target,
	success: function(data, status) {
	    if (status == "success") {
		// this toggles the empty square
		$(this).toggleClass("fa-square-o");
		// this toggles the checked square
		$(this).toggleClass("fa-check-square-o");
	    }
	}
    })
}

// renders a task on the screen
function addTaskToTable(task) {
    
    var finished = "<i class=\"fa fa-square-o task-status\"></i>";
    
    // decides if we need a filled checkbox
    if (task["done"] && task["done"] == true) {
	finished = "<i id=\"task-status\" class=\"fa fa-check-square-o task-status\"></i>";
    }
    
    var row = "<tr>" +
	"<td>" + task["id"] + "</td>" +
	"<td>" + task["title"] + "</td>" +
	"<td>" + task["description"] + "</td>" + 
	"<td>" + finished + "</td>" + 
	"</tr>";

    $("#thetable").append(row);

    // we need to turn off the current click event,
    // and add our new one
    $(".task-status").unbind("click").click(toggleTaskComplete);
}

// sends a new task to the server
function submitTaskToServer(task, callback) {
    $.ajax({
	url: "/todo/api/create_task",
	method: "POST",
	data: task,
	dataType: "json",
	success: callback
    });
}

// loads all the tasks from the server, and renders them
function loadTasksFromServer() {
    $.ajax({
	url: "/todo/api/get_tasks",
	method: "GET",
	dataType: "json",
	success: function(data) {
	    $.each(data["tasks"], function(index, value) {
		addTaskToTable(value);
	    });
	}
    });
}

// submits the form, which adds a new task to the list
function submitForm(e) {
    // stop the form from causing a page refresh
    e.preventDefault();

    // make our new task
    var task = {
	title: $("#title").val(),
	description: $("#description").val()
    };

    // double check if the title is filled
    if ($.trim(task["title"]).length == 0) {
        return;
    }

    // send it to the server
    submitTaskToServer(task, function(data, status) {
	if (status == "success") {
	    addTaskToTable(data["task"]);
	}
    });
}

// this is like the main function of a C/C++ program
$(document).ready(function() {

    // add the client event on the form submit button
    $("#addbutton").click(submitForm);

    // load all the tasks from the server
    loadTasksFromServer();
});

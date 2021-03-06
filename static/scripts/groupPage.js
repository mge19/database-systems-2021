function show_hide(a,b){
  let classname=$(b).attr('class');
  let pos=$('.'+classname).index($(b));
  var x = $('.'+a)[pos];
  if (x.style.display == "none") {
    x.style.display = "block";
    b.value="Hide Group Description";}
  else {
    x.style.display = "none";
    b.value="Show Group Description";}
} 
//get all groups that user is admin
$(document).ready(function () {
    //get all groups that user is admin
    console.log("Admin Group query");
    $.ajax({
        type: "POST",
        url: "/getAdminGroup",
        async: false,
        success: function (data) {
            console.log(data);
            let adminGroup = JSON.parse(data);
            var table = $('.list-group');
            console.log(table.html());
            var inhtml = "<h3 style='text-align:center'>Admin Groups</h3>";
            for(var i=0; i < adminGroup["items"].length; i++){
	   	var group = adminGroup["items"][i];
                var group_name = group["group_name"];
                var group_id = group["group_id"];
		var description = group["description"];
		inhtml += '<li class="list-group-item">' + group_name;
                inhtml += '<form method="POST"><input type="text" name="group_id" style="display:none" value='+group_id+'>'
		inhtml += '<input type="submit" name="remindersButton" value="Group Reminders"><input type="submit" name="tasksButton" value="Group Tasks">';
		inhtml += '<input type="submit" name="updateButton" value="Update Group"><input type="submit" name="deleteButton" value="Delete Group">'
                inhtml += '<input type="submit" name="leaveButton" value="Leave Group">'
		inhtml += '<input type="button" class="show" onclick=show_hide("show_admin",this) value="Show Group Description"></form>';
		inhtml += '<p class="show_admin" style="display:none;">'+description+'</p>';
                inhtml += '</li>';
            }
	    table.append(inhtml)
        },
    });
    //get group that user is not admin
    console.log("Nonadmin group query");
    $.ajax({
        type: "POST",
        url: "/nonAdminGroup",
        async: false,
        success: function (data) {
            console.log(data);
            let nonAdminGroup = JSON.parse(data);
            var table = $('.list-group');
            console.log(table.html());
            var inhtml = "<h3 style='text-align:center'>Nonadmin Groups</h3>";
            for(var i=0; i < nonAdminGroup["items"].length; i++){
	   	var group = nonAdminGroup["items"][i];
                var group_name = group["group_name"];
                var group_id = group["group_id"];
		var description = group["description"];
		inhtml += '<li class="list-group-item">' + group_name;
                inhtml += '<form method="POST"><input type="text" name="group_id" style="display:none" value='+group_id+'>'
		inhtml += '<input type="submit" name="remindersButton" value="Group Reminders"><input type="submit" name="tasksButton" value="Group Tasks">';
		inhtml += '<input type="submit" name="leaveButton" value="Leave Group">'
		inhtml += '<input type="button"  class="showx" onclick=show_hide("show_non_admin",this)  value="Show Group Description"></form>';
		inhtml += '<p class="show_non_admin" style="display:none;">'+description+'</p>';
                inhtml += '</li>';
            }
	    table.append(inhtml)
        },
    });
});

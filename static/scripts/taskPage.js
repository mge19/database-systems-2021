var taskData = {};
function setMinDate(){
    var today=new Date();
    var date=convert_date(String(today.getFullYear()),String(today.getMonth()+1),String(today.getDate()));
    var x=document.getElementsByName("date");
    for(var i=0;i<x.length;i++)
    {
	x[i].setAttribute("min",date);}
}
function show_hide(x){
  var z = document.getElementsByClassName(x);
  if (z[0].style.display == "none") {
    z[0].style.display = "block";} 
  else {
    z[0].style.display = "none";}	
}
function convert_date(year,month,day){
    var new_month=month;
    var new_day=day;
    if(month.length==1){
        new_month="0"+month;}
    if(day.length==1){
        new_day="0"+day;}
    return year+'-'+new_month+'-'+new_day;
}
function convert_time(time){
    var new_time=time;
    if(time.length==4){
        new_time='0'+new_time;}
    return new_time;
}
var months = ["January", "February", "March", "April", "May",
    "June", "July",
    "August", "September",
    "October", "November",
    "December"];
var urgency = ['low', 'medium', 'high'];
//sayfa dolunca tetiklenen fonksiyon
$(document).ready(function () {
    setMinDate();
    //get all tasks to fill calendar
    console.log("Task query");
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:2021/getTasks",
        success: function (data) {
            console.log(data);
            updateVal(JSON.parse(data));
            taskData = JSON.parse(data);
            console.log("DATA updated");
	    setupCalendar();
        },
    });
    //get upcoming tasks to fill left side pane
    console.log("Upcoming Task query");
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:2021/upcomingTasks",
        success: function (data) {
            let updates = JSON.parse(data);
            console.log("UPDATES: ", updates);
            var table = $('.taskList');
            console.log(table.html());
            table.empty();
            var inhtml = "<li><h3>Upcoming tasks</h3></li>" +
                "<li>";
            for (var i = 0; i < updates["items"].length; i++) {
                    var task = updates["items"][i];
                    day = task["day"];
                    month = task["month"];
                    year = task["year"];
                    inhtml += '<ul class="sets">';
                    inhtml += '<li class="head" onclick=show_hide("show'+i+'")>' + day + '-' + month + '-' + year + '</li>';
                    inhtml += '<li class="show'+i+'" style="display:none">' + task["title"] + '<br><br>' + task["urgency"];
		    inhtml += '<br><br>' + task["message"]+'</li>';
            }
            inhtml += '</ul>';
            console.log(inhtml);
            table.append(inhtml);
        },
    });
});

//input fieldlarin degerlerini doldurmak
$(document).ready(function () {
    let i = 1;
    for (i; i <= 31; i++) {
        snippet = `<option value="${i}">${i}</option>`
        $('.days').append(snippet); 
    }
    for (i = 0; i < months.length; i++) {
        snippet = `<option value="${months[i]}">${months[i]}</option>`
        $('.months').append(snippet); 
    }
    for(i = 0; i < 3; i++) {
	snippet = `<option value="${urgency[i]}">${urgency[i]}</option>`
        $('.urgency').append(snippet); 
    }
});


//arama tiplerinde degisiklik
$(document).ready(function () {
    $('#searchType').on('change', function (e) {
        e.preventDefault();

        console.log(this.value);
        $(this).siblings().removeClass('active-flex');

        selector = "." + this.value
        $(selector).addClass('active-flex');
    });
});

//search butonuna basinca tetiklenen fonksiyon
$(document).ready(function () {
    $('.queries button').on('click', function (e) {
        e.preventDefault();

        console.log($('#searchType').val());
        var dict = {};
        switch ($('#searchType').val()) {
            case "ydiv":
                console.log($(".ydiv > .year").val());
                dict["type"] = "0";
                dict["year"] = $(".ydiv > .year").val();
                break;
            case "ymdiv":
                console.log($(".ymdiv > .year").val());
                console.log($(".ymdiv > .months").val());
                dict["type"] = "1";
                dict["year"] = $(".ymdiv > .year").val();
                dict["months"] = months.indexOf($(".ymdiv > .months").val()) + 1;
                break;
            case "ymddiv":
                console.log($(".ymddiv > .year").val());
                console.log($(".ymddiv > .months").val());
                console.log($(".ymddiv > .days").val());
                dict["type"] = "2";
                dict["year"] = $(".ymddiv > .year").val();
                dict["months"] = months.indexOf($(".ymddiv > .months").val()) + 1;
                dict["days"] = $(".ymddiv > .days").val();
                break;
            case "tdiv":
                console.log($(".tdiv > #title").val());
                dict["type"] = "3";
                dict["title"] = $(".tdiv > #title").val();
                break;
        }
        console.log("Sending search query:", dict);
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:2021/searchTasks",
            data: dict,
            success: function (data) {
                console.log("AJAX RETURN: ", data);
                searchTable = JSON.parse(data);
                //update the table
                var table = $('#book-list');
                table.empty();
                var inhtml = "";
                for (var i = 0; i < searchTable["items"].length; i++) {
                    var task = searchTable["items"][i];
                    inhtml += "<tr><td>" + task["day"] + "." + task["month"] + "." + task["year"] + "</td><td>" + task["time"] + "</td>   <td>" + task["title"] + "</td><td>" + task["urgency"] + "</td>"
                    inhtml += '<td><a href="#" class="btn btn-primary btn-sm show">Show</a></td>'
                    inhtml += '<td><a href="#" class="btn btn-danger btn-sm delete">Delete</a></td>';
		    inhtml += '<td><a href="#" class="btn btn-success btn-sm update">Update</a></td></tr>';
		    inhtml += '<tr style="display:none" id=' + i + '><td>' + task["message"] + '</td></tr>';                
		    inhtml += '<tr style="display:none" id="update' + i + '"><td><strong>Update a task</strong><br><br>';
		    inhtml += '<form method="post"><label for="date">New Date</label><input type="date" name="date" value="'+convert_date(String(task["year"]),String(task["month"]),String(task["day"]))+'"><br><br>';
		    inhtml += '<label for="time">New Time</label><input type="time" name="time" value="'+convert_time(task["time"])+'"><br><br>';
		    inhtml += '<label for="urgency">New Urgency</label><select name="urgency" class="urgency">';
		    for(var j=0 ; j < 3 ; j++) {
		        if(urgency[j]==task["urgency"]){
				inhtml += '<option selected value="'+ urgency[j] + '">' + urgency[j] + '</option>';}
		        else{
				inhtml += '<option value="'+ urgency[j] + '">' + urgency[j] + '</option>';}		    
		    }
		    inhtml += '</select><br><label for="title">New Title</label><input type="text" name="title" value="' + task["title"] + '" placeholder="New Title" required ><br><br>';
		    inhtml += '<label for="message">New Message</label><textarea name="message" placeholder="New Message" required >' + task["message"] + '</textarea><br><br>';	
		    inhtml += '<input type="submit" id="updateButton'+i+'" value="Update" class="btn btn-success btn-block add-btn"></form></td></tr>';
                }
                table.append(inhtml);
            },
        });     
    });
});


//Tabloda ki show, delete butonlari fonksiyonlari
$(document).ready(function () {
    var $parent = $("#book-list");
    //show button
    $parent.on('click', '.show', function (e) {
        e.preventDefault();
        e.stopPropagation();
	let pos = $('.show').index($(this));
        console.log(pos);
        let desc = $('#' + pos);
	if($(this).html()=="Show"){
		desc.css('display','block');
		$(this).html('Hide');}
	else{
		desc.css('display','none');
		$(this).html('Show');}
	
    });
    $parent.on('click', '.delete', function (e) {
        e.preventDefault();
        let pos = $('.delete').index($(this));
        let taskid = searchTable["items"][pos]["alert_id"];
        $(this).closest("tr").remove();
        searchTable["items"].splice(pos, 1);
        console.log(taskid);
        //send query to remove id

        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:2021/deleteUserAlert",
            data: {
                value: taskid
            },
            success: function (data) {
                console.log("AJAX RETURN: ", data);
            },
        });     
    });
    $parent.on('click', '.update', function (e) {
	setMinDate();
        e.preventDefault();
        e.stopPropagation();
	let pos = $('.update').index($(this));
        let form = $('#update' + pos);
	if($(this).html()=="Update"){
	        form.css('display','block');
		$(this).html("Don't Update");}
	else{
		form.css('display','none');
		$(this).html('Update');} 
                $parent.on('click', '#updateButton'+pos, function (e2) {
		    e2.preventDefault();
	     	    var dict="";
		    let form=$(this).closest('form');
	     	    let taskid = searchTable["items"][pos]["alert_id"];	
	     	    dict+=taskid+',';
		    form.find( '[name]' ).each( function(){
		       let value=$(this).val();
		       dict+=value+',';});
             	$.ajax({
         	   type: "POST",
         	   url: "http://127.0.0.1:2021/updateUserAlert",
         	   data:{	
		     value:dict,
		   },
            	   success: function (data) {
                       console.log("AJAX RETURN: ", data);
            	   },
                });
            }); 	
    });
});



$(document).ready(function () {
    //get user
    var size = 0;
    $.ajax({
        type: "POST",
        url: "/getUser",
        async: false,
        success: function (data) {
            console.log(data);
            let users = JSON.parse(data);
            console.log("USERS: ", users);
            var table = $('.userlist');
            var inhtml = "";
            for (var i = 0; i < users["items"].length; i++) {
                var user = users["items"][i];
                var user_name = user["first_name"];
		var user_last_name=user["last_name"];
                var user_mail = user["email"];
                var user_id = user["user_id"];
                inhtml += '<div class="form-check"><p class="mainp">' + user_name + ' ' + user_last_name + '(' + user_mail + ')</p>';
                inhtml += '<input class="form-check-input user" type="checkbox" name="nonadmin" id="nonadminRadio" value=' + user_id + '>  <label class="form-check-label" for="nonadminRadio">Nonadmin</label>';
		inhtml += '<input class="form-check-input admin" type="checkbox" name="admin" id="adminRadio" value=' + user_id + ' >  <label class="form-check-label" for="adminRadio">Admin</label>';
                inhtml += '</div > ';
                size++;
            }
            table.append(inhtml);
        },
    });
});


$(document).ready(function () {
    $("#submitButton").click(function () {
        console.log("clicked");
        $.ajax({
            type: "POST",
            url: "/group_update",
            async: false,
        });
    });

});

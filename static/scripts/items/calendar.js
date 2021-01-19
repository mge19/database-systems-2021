function setupCalendar() {
    var date = new Date();
    var today = date.getDate();
    // Set click handlers for DOM elements
    $(".right-button").click({ date: date }, next_year);
    $(".left-button").click({ date: date }, prev_year);
    $(".month").click({ date: date }, month_click);
    $("#add-button").click({ date: date }, new_event);
    // Set current month as active
    $(".months-row").children().eq(date.getMonth()).addClass("active-month");
    init_calendar(date);
    var reminders = check_events(today, date.getMonth() + 1, date.getFullYear());
    display_events(reminders, calendar_months[date.getMonth()], today);
}
$(document).ready(function () {
    setupCalendar();
});
// Initialize the calendar by appending the HTML dates
// Burda yuvarlaklar yok
function init_calendar(date) {
    $(".tbody").empty();
    $(".events-container").empty();
    var calendar_days = $(".tbody");
    var month = date.getMonth();
    var year = date.getFullYear();
    var day_count = days_in_month(month, year);
    var row = $("<tr class='table-row'></tr>");
    var today = date.getDate();
    // Set date to 1 to find the first day of the month
    date.setDate(1);
    var first_day = date.getDay();
    // 35+firstDay is the number of date elements to be added to the dates table
    // 35 is from (7 days in a week) * (up to 5 rows of dates in a month)
    for (var i = 0; i < 35 + first_day; i++) {
        // Since some of the elements will be blank, 
        // need to calculate actual date from index
        var day = i - first_day + 1;
        // If it is a sunday, make a new row
        if (i % 7 === 0) {
            calendar_days.append(row);
            row = $("<tr class='table-row'></tr>");
        }
        // if current index isn't a day in this month, make it blank
        if (i < first_day || day > day_count) {
            var curr_date = $("<td class='table-date nil'>" + "</td>");
            row.append(curr_date);
        }
        else {
            var curr_date = $("<td class='table-date'>" + day + "</td>");
            var events = check_events(day, month + 1, year);
            if (today === day && $(".active-date").length === 0) {
                curr_date.addClass("active-date");
                display_events(events, calendar_months[month], day);
            }
            // If this date has any events, style it with .event-date
            if (events.length !== 0) {
                curr_date.addClass("event-date");
            }
            // Set onClick handler for clicking a date
            curr_date.click({ events: events, month: calendar_months[month], day: day }, date_click);
            row.append(curr_date);
        }
    }
    // Append the last row and set the current year
    calendar_days.append(row);
    $(".year").text(year);
}

// Get the number of days in a given month/year
function days_in_month(month, year) {
    var monthStart = new Date(year, month, 1);
    var monthEnd = new Date(year, month + 1, 1);
    return (monthEnd - monthStart) / (1000 * 60 * 60 * 24);
}

// Event handler for when a date is clicked
function date_click(event) {
    $(".events-container").show(250);
    $("#dialog").hide(250);
    $(".active-date").removeClass("active-date");
    $(this).addClass("active-date");
    display_events(event.data.events, event.data.month, event.data.day); //burasi dogru. event.data.events kalacak
};

// Event handler for when a month is clicked
function month_click(event) {
    $(".events-container").show(250);
    $("#dialog").hide(250);
    var date = event.data.date;
    $(".active-month").removeClass("active-month");
    $(this).addClass("active-month");
    var new_month = $(".month").index(this);
    date.setMonth(new_month);
    init_calendar(date);
}

// Event handler for when the year right-button is clicked
function next_year(event) {
    $("#dialog").hide(250);
    var date = event.data.date;
    var new_year = date.getFullYear() + 1;
    $("year").html(new_year);
    date.setFullYear(new_year);
    init_calendar(date);
}

// Event handler for when the year left-button is clicked
function prev_year(event) {
    $("#dialog").hide(250);
    var date = event.data.date;
    var new_year = date.getFullYear() - 1;
    $("year").html(new_year);
    date.setFullYear(new_year);
    init_calendar(date);
}

// Event handler for clicking the new event button
function new_event(event) {
    // if a date isn't selected then do nothing
    if ($(".active-date").length === 0)
        return;
    // remove red error input on click
    $("input").click(function () {
        $(this).removeClass("error-input");
    })
    // empty inputs and hide events
    $("#dialog input[type=text]").val('');
    $("#dialog input[type=number]").val('');
    $(".events-container").hide(250);
    $("#dialog").show(250);
    // Event handler for cancel button
    $("#cancel-button").click(function () {
        $("#name").removeClass("error-input");
        $("#count").removeClass("error-input");
        $("#dialog").hide(250);
        $(".events-container").show(250);
    });
    // Event handler for ok button
    $("#ok-button").unbind().click({ date: event.data.date }, function () {
        var date = event.data.date;
        var name = $("#name").val().trim();
        var count = parseInt($("#count").val().trim());
        var day = parseInt($(".active-date").html());
        // Basic form validation
        if (name.length === 0) {
            $("#name").addClass("error-input");
        }
        else if (isNaN(count)) {
            $("#count").addClass("error-input");
        }
        else {
            $("#dialog").hide(250);
            console.log("new event");
            new_event_json(name, count, date, day);
            date.setDate(day);
            init_calendar(date);
        }
    });
}

// Adds a json event to event_data
function new_event_json(name, count, date, day) {
    var event = {
        "occasion": name,
        "invited_count": count,
        "year": date.getFullYear(),
        "month": date.getMonth() + 1,
        "day": day
    };
    event_data["events"].push(event);
}

//Herhangi bir gune t�klan�ld���nda sa� panelde eventleri s�ralayan fonksiyon
function display_events(items, month, day) {
    console.log("triggered");
    $(".events-container").empty();
    $(".events-container").show(250);
    // If there are no events for this date, notify the user
    if (items.length === 0) {
        var event_card = $("<div class='event-card'></div>");
        var event_name = $("<div class='event-name'>There are no events planned for " + month + " " + day + ".</div>");
        $(event_card).css({ "border-left": "10px solid #000000" });
        $(event_card).append(event_name);
        $(".events-container").append(event_card);
    }
    else {
        // Go through and add each reminder as a card to the events container
        for (var i = 0; i < items.length; i++) {
            var event_card = $("<div class='event-card'></div>");
            var item_title = $("<div class='event-name'>" + items[i]["title"] + ":</div>");
            var item_context = $("<p>" + items[i]["message"] + "</p>");
            item_context.addClass("event-contentp");
	    var urgency = $("<p>" + items[i]["urgency"] + "</p>");
	    urgency.addClass("urgencyp");
            var hourmin = $("<p>" + items[i]["time"] + "</p>");
            hourmin.addClass("event-timep");
            var hr = $("<hr class=event-hr>");
            $(event_card).append(item_title).append(hr).append(item_context).append(urgency).append(hourmin);
            $(".events-container").append(event_card);
        }
    }

}

// Checks if a specific date has any events
function check_events(day, month, year) {
    var items = [];
    if(typeof(event_data["items"])!="undefined"){
	for (var i = 0; i < event_data["items"].length; i++) {
            var item = event_data["items"][i];
            if (item["day"] === day && item["month"] === month && item["year"] === year) {
            	items.push(item);
            }
	}
    }
    return items;
}
function updateVal(data) {
    event_data = data;
    console.log(event_data);
}
// Given data for events in JSON format


const calendar_months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
];

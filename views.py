import os
import datetime
from flask import abort, current_app, render_template, flash
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import Flask
from json import dumps
import sql_functions as sf
active_user=0
active_group=0
app = Flask(__name__)
def next_weekday(weekday, time, mode, iteration = 10): #get upcoming weekday dates.  # 0 = Monday, 1=Tuesday, 2=Wednesday...
#usage weekday = (0 = Monday, 1=Tuesday, 2=Wednesday...), time = 00:00:00, mode = (0 = Daily, 1 = Weekly, 2 = BiWeekly, 4 = Monthly,) iteration = total dates to return
    d = datetime.datetime.now()    
    days_ahead = weekday - d.weekday()
    print(days_ahead)
    split_time = str(time).split(':')
    print(split_time)
    print(weekday)
    print(time)
    print(type(mode))
    print(iteration)
    mode = int(mode)
    for i in range(2):
        split_time[i] = int(split_time[i])

    d = d.replace(hour=split_time[0], minute=split_time[1], second=0, microsecond=0)
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    weekday = d + datetime.timedelta(days_ahead)
    dates = []
    if mode == 0:
        delta = datetime.timedelta(days=1)
        for i in range(iteration):
            dates.append(d)
            d = d + delta
    elif mode == 1:
        delta = datetime.timedelta(days=7)
        for i in range(iteration):
            dates.append(weekday)
            weekday = weekday + delta
    elif mode == 2:
        delta = datetime.timedelta(days=14)
        for i in range(iteration):
            dates.append(weekday)
            weekday = weekday + delta
    elif mode == 3:
        delta = datetime.timedelta(days=28)
        for i in range(iteration):
            dates.append(weekday)
            weekday = weekday + delta
    print(dates)
    return dates
    
def convert_to_json(listOfList):
    print(listOfList)
    try:
        m = len(listOfList)
        n = len(listOfList[0])
    except:
        print("Empty list")
        return 0
    json = {}
    json["items"] = []

    print("converting....")
    col_names = []
    for i in range(n):
        col_name = str(listOfList[0][i])
        col_names.append(col_name)
    
    for i in range(1,m):
        sub_json = {}
        for j in range(n):
            if(isinstance(listOfList[i][j],datetime.datetime)):
                
                sub_json["year"] = listOfList[i][j].year
                sub_json["month"] = listOfList[i][j].month
                sub_json["day"] = listOfList[i][j].day
                
                if(len(str(listOfList[i][j].minute)) == 1):
                    sub_json["time"] = str(listOfList[i][j].hour) + ":0" + str(listOfList[i][j].minute)
                else:
                    sub_json["time"] = str(listOfList[i][j].hour) + ":" + str(listOfList[i][j].minute)

                continue
            sub_json[col_names[j]] = str(listOfList[i][j])
        json["items"].append(sub_json)
    

    print(json)
    return json
def main_page():
    if not session.get('logged_in'):   
        return redirect(url_for("login_page"))
    else:                
        if request.method == 'GET':
            print(session)
            return render_template("mainPage.html")
        else: #method == POST
            flash("test")
            print(session)
            return redirect(url_for("main_page"))

def login_page():
    if request.method == 'GET':
        print(session)
        if session.get('logged_in'):
            return redirect(url_for("main_page"))
        return render_template("auth.html")
    
    
    else:  #method == POST
        register = False
        login = False
        if(request.form['button'] == "register"):
            print("register is active")
            register = True
        elif(request.form['button'] == "login"):
            print("login is active")
            login = True
        else:
            print("invalid form request")
            return redirect(url_for("login_page"))

        if(register):
            register_first_name = request.form['register-first-name'] if(request.form['register-first-name']) else None
            register_last_name = request.form['register-last-name'] if(request.form['register-last-name']) else None
            register_email = request.form['register-email'] if(request.form['register-email']) else None
            register_password = request.form['register-password'] if(request.form['register-password']) else None
            if(len(register_password) < 6):
                print("password should be longer than 6 characters")
                flash("password should be longer than 6 characters")
                return redirect(url_for("login_page"))
            database_result = sf.add_user(register_first_name, register_last_name, register_email, register_password)
            print(database_result)
            if(database_result == -3):
                print("registered successfully, login to access your account")
                flash("registered successfully, login to access your account")
                return redirect(url_for("login_page"))
            else:
                print("not registered successfully")
                flash("not registered successfully")
                return redirect(url_for("login_page"))
        if(login):
            login_email = request.form['login-email'] if(request.form['login-email']) else None
            login_password = request.form['login-password'] if(request.form['login-password']) else None
            print(login_password)
            
            database_result = sf.get_user_password(login_email)
            print(database_result)

            if(database_result == -1):
                print("User not found")
                flash("User not found")
                return redirect(url_for("login_page"))
            else: # password belong to email address is obtained  
                password_belong_to_email = database_result[1][0]
                if(password_belong_to_email!=login_password):
                    print("Wrong password")
                    flash("Wrong password")
                    return redirect(url_for("login_page"))
                session['user_id'] = sf.get_user_id(login_email)[1][0]
                global active_user
                active_user=session['user_id']
                print(active_user)
                session['logged_in'] = True
                print(session)
                return redirect(url_for("main_page"))

def logout_page():
    print("You have logged out.")
    flash("You have logged out.")
    session['user_id'] = None
    session['logged_in'] = False
    return redirect(url_for("login_page"))

def change_password_page():
    if not session.get('logged_in'):   
        return redirect(url_for("login_page"))
    else:
        if request.method == 'GET':
            print("change_password_page with get")
            print(session['user_id'])
            return render_template("ChangePassword.html")
        else: 
            error=False
            current_password = request.form['current-password']
            new_password = request.form['new-password']
            confirm_password = request.form['confirm-password']
            print(request.form)
            if(current_password == "" or new_password == "" or confirm_password == ""):
                    print("please enter all the information requested")
                    flash("please enter all the information requested")
                    error=True
            if(len(new_password) < 6 or len(confirm_password) < 6):
                    print("password should be longer than 6 characters")
                    flash("password should be longer than 6 characters")
                    error=True
            if(current_password == new_password):
                print("new password cannot be the same")
                flash("new password cannot be the same")
                error=True
            if(confirm_password != new_password):
                print("New password fields should be same")
                print("New password fields should be same")
                error=True
            user_id = session['user_id']
            user_info = sf.get_user_info(user_id)
            email_belong_to_user = user_info[1][3]
            print(email_belong_to_user)
            password_belong_to_user = sf.get_user_password(email_belong_to_user)
            print(password_belong_to_user)
            if(password_belong_to_user == -1):
                print("database error, contact customer service")
                flash("database error, contact customer service")
                error=True
            password_belong_to_user = password_belong_to_user[1][0] 
            if(password_belong_to_user!=current_password):
                print("current password you have given is not correct")
                flash("current password you have given is not correct")
                error=True
            if error:
                return redirect(url_for("change_password_page"))
            db_result = sf.update_user_password(user_id, new_password)
            if(db_result != -3):
                print("database error, contact customer service")
                flash("database error, contact customer service")
                error=True
            if error:
                return redirect(url_for("change_password_page"))
            print("password is changed, relogin now")
            flash("password is changed, relogin now")
            session['user_id'] = None
            session['logged_in'] = False
            return redirect(url_for("login_page"))
def edit_profile_page():
    if not session.get('logged_in'):   
        return redirect(url_for("login_page"))
    else:
        if request.method=='GET':
            return render_template("editProfile.html")
        else:
            error=False
            user_id=session['user_id']
            new_first_name=request.form['new-first-name']
            new_last_name=request.form['new-last-name']
            new_email=request.form['new-email']
            user_info = sf.get_user_info(user_id)
            first_name=user_info[1][1]
            last_name=user_info[1][2]
            email = user_info[1][3]
            if new_first_name=="" and new_last_name=="" and new_email=="":
                print("Please fill at least one information.")
                flash("Please fill at least one information.")
                return redirect(url_for('edit_profile_page'))
            if new_first_name==first_name:
                print("New first name should be different")
                flash("New first name should be different")
                error=True
            if new_last_name==last_name:
                print("New last name should be different")
                flash("New last name should be different")
                error=True
            if new_email==email:
                print("New e-mail should be different")
                flash("New e-mail should be different")
                error=True
            if error:
                return redirect(url_for('edit_profile_page'))
            if new_first_name!='':
                sf.update_user_first_name(user_id,new_first_name)
            if new_last_name!='':
                sf.update_user_last_name(user_id,new_last_name)
            if new_email!='':
                sf.update_user_email(user_id,new_email)
            return redirect(url_for("main_page"))
def reminder_page():
    if not session.get('logged_in'):   
        return redirect(url_for("login_page"))
    else:                
        if request.method == 'GET':
            print("At reminder get")
            return render_template("reminderPage.html")
        else: 
            print("method is post")
            user_id = session.get("user_id")
            print(user_id)
            print(request.form)
            if 'toggler' in request.form:
                time = request.form['time1']
                title = request.form['title1']
                message = request.form['message1']
                urgency = request.form['urgency1']
                days = int(request.form['days'])
                interval = request.form['interval']
                print("Interval: " + interval)
                if days == "Monday": day = 0
                elif days == "Tuesday": day = 1
                elif days == "Wednesday": day = 2
                elif days == "Thursday": day = 3
                elif days == "Friday": day = 4
                elif days == "Saturday": day = 5
                elif days == "Sunday": day = 6
                mode = interval
                reminder_days = next_weekday(days, time, mode, iteration=5) #change iteration to add more repeating reminders
                print(reminder_days)
                for datetime in reminder_days:
                    print("added: " + str(datetime))
                    sf.add_user_reminder(user_id,datetime,title,message,urgency)
            else:
                time = request.form['time']
                title = request.form['title']
                message = request.form['message']
                urgency = request.form['urgency']
                date = request.form['date']
                button=request.form['button']
                datetime = date + " " + time
                print("Date: " + date)    
                print(datetime)
                print("title: " + title)
                if button=='Submit':
                    sf.add_user_reminder(user_id, datetime, title, message, urgency)    
            return redirect(url_for("reminder_page"))

         
def task_page():
    if not session.get('logged_in'): 
        print("test session")
        return redirect(url_for("login_page"))
    else:
        if request.method == 'GET':
            print("method is get")
            return render_template("taskPage.html")
        else: 
            print("method is post")
            button=request.form['button']
            user_id = session.get("user_id")
            print(user_id)
            date = request.form['date']
            time = request.form['time']
            datetime = date + " " + time
            title = request.form['title']
            message = request.form['message']
            urgency = request.form['urgency']
            print(request.form)
            print(datetime)
            if button=='Submit':
                sf.add_user_task(user_id, datetime, title, message, urgency)
            return redirect(url_for("task_page"))

def deleteUserAlert():
    alert_id=request.values.get('value')
    sf.delete_user_alert(alert_id)
    return alert_id

def updateUserAlert():
    data=request.values.get('value').split(',')
    datetime = data[1] + " " + data[2]
    sf.update_user_alert(data[0],datetime,data[4],data[5],data[3])
    return data[0]
    
def deleteGroupAlert():
    alert_id=request.values.get('value')
    sf.delete_group_alert(alert_id)
    return alert_id

def updateGroupAlert():
    data=request.values.get('value').split(',')
    datetime = data[1] + " " + data[2]
    sf.update_group_alert(data[0],datetime,data[4],data[5],data[3])
    return data[0]

def group_page():
    if not session.get('logged_in'):   
        return redirect(url_for("login_page"))
    print(session)
    if request.method=='GET':
        return render_template("groupPage.html")
    else:
        global active_group
        if 'joinButton' in request.form:
            group_name=request.form['group_name']
        else:
            active_group=request.form['group_id']
        print(active_group)
        if 'remindersButton' in request.form:
            return redirect(url_for("group_reminders_page"))
        if 'tasksButton' in request.form:
            return redirect(url_for("group_tasks_page"))
        if 'updateButton' in request.form:
            return redirect(url_for("group_update_page"))
        if 'deleteButton' in request.form:
            data=sf.delete_group(active_group)
            return redirect(url_for("group_page"))
        if 'leaveButton' in request.form:
            data=sf.leave_group(active_user,active_group)
            return redirect(url_for("group_page"))
        if 'joinButton' in request.form:
            data=sf.join_group(active_user,group_name)
            if data=='0':
                print("Group not found.")
                flash("Group not found.")
            elif data=='1':
                print("User is already joined the group.")
                flash("User is already joined the group.")
            return redirect(url_for("group_page"))   
def group_create_page():
    if not session.get('logged_in'):   
        return redirect(url_for("login_page"))
    else:                
        if request.method == 'GET':
            print("group_create_page is opened and method is get")
            return render_template("createGroupPage.html")
        else: #method == POST
            data=request.get_data().decode("utf-8")
            data=data.split('&')
            nonadmins=set()
            admins=set()
            for x in data:
                if x[0:6]=="admin=":
                    admins.add(x[6:])
                elif x[0:9]=="nonadmin=":
                    nonadmins.add(x[9:])
            nonadmins=nonadmins-admins
            print(nonadmins)
            print(admins)
            group_name = request.form['group_name']
            description = request.form['description']
            print(group_name)
            print(description)
            if len(admins)>0:
                sf.create_group(group_name, description, admins, nonadmins)
                return redirect(url_for("group_page"))
            else:
                print("A group must contain at at least one admin.")
                flash("A group must contain at least one admin.")
                return redirect(url_for("group_create_page"))
            
def group_tasks_page():
    print(session)
    if not session.get('logged_in'): 
        print("test session")
        return redirect(url_for("login_page"))
    else:
        if request.method == 'GET':
            print("method is get")
            return render_template("groupTaskPage.html")
        else: #method == POST
            print("method is post")
            button=request.form['button']
            date = request.form['date']
            time = request.form['time']
            datetime = date + " " + time
            title = request.form['title']
            message = request.form['message']
            urgency = request.form['urgency']
            print(request.form)
            print(datetime)
            if button=='Submit':
                sf.add_group_task(active_group, datetime, title, message, urgency)
        return redirect(url_for("group_tasks_page"))

def group_reminders_page():
    if not session.get('logged_in'):   
        return redirect(url_for("login_page"))
    else:                
        if request.method == 'GET':
            print("At reminder get")
            return render_template("groupReminderPage.html")
        else: 
            print("method is post")
            print(request.form)
            if 'toggler' in request.form:
                time = request.form['time1']
                title = request.form['title1']
                message = request.form['message1']
                urgency = request.form['urgency1']
                days = int(request.form['days'])
                interval = request.form['interval']
                print("Interval: " + interval)
                if days == "Monday": day = 0
                elif days == "Tuesday": day = 1
                elif days == "Wednesday": day = 2
                elif days == "Thursday": day = 3
                elif days == "Friday": day = 4
                elif days == "Saturday": day = 5
                elif days == "Sunday": day = 6
                mode = interval
                reminder_days = next_weekday(days, time, mode, iteration=5) #change iteration to add more repeating reminders
                print(reminder_days)
                for datetime in reminder_days:
                    print("added: " + str(datetime))
                    sf.add_group_reminder(active_group,datetime,title,message,urgency)
            else:
                time = request.form['time']
                title = request.form['title']
                message = request.form['message']
                urgency = request.form['urgency']
                date = request.form['date']
                button=request.form['button']
                datetime = date + " " + time
                print("Date: " + date)    
                print(datetime)
                print("title: " + title)
                if button=='Submit':
                    sf.add_group_reminder(active_group, datetime, title, message, urgency)
            return redirect(url_for("group_reminders_page"))
            
def group_update_page():
    if not session.get('logged_in'):   
        return redirect(url_for("login_page"))
    else:                
        if request.method == 'GET':
            print("group_update_page is opened and method is get")
            return render_template("updateGroupPage.html")
        else: #method == POST
            data=request.get_data().decode("utf-8")
            data=data.split('&')
            nonadmins=set()
            admins=set()
            for x in data:
                if x[0:6]=="admin=":
                    admins.add(x[6:])
                elif x[0:9]=="nonadmin=":
                    nonadmins.add(x[9:])
            nonadmins=nonadmins-admins
            print(nonadmins)
            print(admins)
            new_group_name = request.form['new_group_name']
            new_description = request.form['new_description']
            print(new_group_name)
            print(new_description)
            if len(admins)>0:
                sf.update_group(active_group,new_group_name, new_description, admins, nonadmins)
                return redirect(url_for("group_page"))
            else:
                print("A group must contain at least one admin.")
                flash("A group must contain at least one admin.")
                return redirect(url_for("group_update_page"))

def getReminders():
    print("At get reminders")
    result = sf.get_user_reminders(active_user)
    return dumps(convert_to_json(result))    

def getTasks():
    print("At get tasks")
    result = sf.get_user_tasks(active_user)
    return dumps(convert_to_json(result))

def searchTasks():
    print("At search tasks")
    #print(request.values)
    d = datetime.datetime.now()    
    type = int(request.values.get('type'))
    days = 1
    months = 1
    if(type == 0):
        year = int(request.values.get('year'))
        print(year)
        d = d.replace(year=year, month=months, day=days, hour=0, minute=0, second=0, microsecond=0)
        result = sf.search_user_task_date(active_user,d,0)
    elif(type == 1):
        year = int(request.values.get('year'))
        months = int(request.values.get('months'))
        d = d.replace(year=year, month=months, day=days, hour=0, minute=0, second=0, microsecond=0)
        result = sf.search_user_task_date(active_user,d,1)
    elif(type == 2): 
        year = int(request.values.get('year'))
        months = int(request.values.get('months'))
        days = int(request.values.get('days'))
        print(days, months, year)
        d = d.replace(year=year, month=months, day=days, hour=0, minute=0, second=0, microsecond=0)
        result = sf.search_user_task_date(active_user,d,2)
    elif(type == 3): 
        title = request.values.get('title')
        result = sf.search_user_task_title(active_user, title)
    print(result)   
    return dumps(convert_to_json(result))

def searchReminders():
    print("At search reminders")
    d = datetime.datetime.now()    
    months = 1
    days = 1
    type = int(request.values.get('type'))
    if(type == 0):
        year = int(request.values.get('year'))
        d = d.replace(year=year, month=months, day=days, hour=0, minute=0, second=0, microsecond=0)
        result = sf.search_user_reminder_date(active_user,d,0)
    elif(type == 1):
        year = int(request.values.get('year'))
        months = int(request.values.get('months'))
        print(year, months, days)
        d = d.replace(year=year, month=months, day=days, hour=0, minute=0, second=0, microsecond=0)
        result = sf.search_user_reminder_date(active_user,d,1)
    elif(type == 2):
        year = int(request.values.get('year'))
        months = int(request.values.get('months'))
        days = int(request.values.get('days'))
        print(year, months, days)
        d = d.replace(year=year, month=months, day=days, hour=0, minute=0, second=0, microsecond=0)
        result = sf.search_user_reminder_date(active_user,d,2)
    elif(type == 3):
        title = request.values.get('title')
        result = sf.search_user_reminder_title(active_user,title)
    return dumps(convert_to_json(result))

def getUser(): 
    result = sf.get_all_users()
    return dumps(convert_to_json(result))


def getAdminGroup(): 
    result = sf.get_user_admin_groups(active_user)
    result = convert_to_json(result)
    print(result)
    return dumps(result)


def nonAdminGroup(): 
    result = sf.get_user_nonadmin_groups(active_user)
    result = convert_to_json(result)
    print(result)
    return dumps(result)

def upcomingGroupTasks(): 
    result = sf.get_upcoming_group_tasks(active_group)
    return dumps(convert_to_json(result))


def getGroupTasks(): 
    result = sf.get_group_tasks(active_group)
    return dumps(convert_to_json(result))

def getGroupReminders(): 
    result = sf.get_group_reminders(active_group)
    return dumps(convert_to_json(result))


def searchGroupReminders():
    d = datetime.datetime.now()    
    months = 1
    days = 1
    type = int(request.values.get('type'))
    if(type == 0):
        year = int(request.values.get('year'))
        d = d.replace(year=year, month=months, day=days, hour=0, minute=0, second=0, microsecond=0)
        result = sf.search_group_reminder_date(active_group,d,0)
    elif(type == 1): 
        year = int(request.values.get('year'))
        months = int(request.values.get('months'))
        print(year, months, days)
        d = d.replace(year=year, month=months, day=days, hour=0, minute=0, second=0, microsecond=0)
        result = sf.search_group_reminder_date(active_group,d,1)
    elif(type == 2):
        year = int(request.values.get('year'))
        months = int(request.values.get('months'))
        days = int(request.values.get('days'))
        print(year, months, days)
        d = d.replace(year=year, month=months, day=days, hour=0, minute=0, second=0, microsecond=0)
        result = sf.search_group_reminder_date(active_group,d,2)
    elif(type == 3): 
        title = request.values.get('title')
        result = sf.search_group_reminder_title(active_group, title)
    return dumps(convert_to_json(result))


def searchGroupTasks(): 
    print("At search tasks")
    d = datetime.datetime.now()    
    type = int(request.values.get('type'))
    days = 1
    months = 1
    if(type == 0):
        year = int(request.values.get('year'))
        print(year)
        d = d.replace(year=year, month=months, day=days, hour=0, minute=0, second=0, microsecond=0)
        result = sf.search_group_task_date(active_group,d,0)
    elif(type == 1):
        year = int(request.values.get('year'))
        months = int(request.values.get('months'))
        d = d.replace(year=year, month=months, day=days, hour=0, minute=0, second=0, microsecond=0)
        result = sf.search_group_task_date(active_group,d,1)
    elif(type == 2): 
        year = int(request.values.get('year'))
        months = int(request.values.get('months'))
        days = int(request.values.get('days'))
        print(days, months, year)
        d = d.replace(year=year, month=months, day=days, hour=0, minute=0, second=0, microsecond=0)
        result = sf.search_group_task_date(active_group,d,2)
    elif(type == 3): 
        title = request.values.get('title')
        result = sf.search_group_task_title(active_group, title)
    print(result)   
    return dumps(convert_to_json(result))	

def upcomingTasks():
    print("Received update request")
    result = sf.get_upcoming_user_tasks(active_user)
    return dumps(convert_to_json(result))

from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import session
import views
import os


template_dir = os.path.abspath('./static/html')
def create_app():
    app = Flask('myapp',  template_folder=template_dir)
    app.secret_key = "c105493b0d3d3d23394b9be42dbb16aa428aa72ea0492652" #secret key needed for cookies

    app.add_url_rule("/", view_func=views.main_page, methods=["GET","POST"])
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET","POST"])
    app.add_url_rule("/logout", view_func=views.logout_page, methods=["GET","POST"])
    app.add_url_rule("/change_password", view_func=views.change_password_page, methods=["GET","POST"])
    app.add_url_rule("/task", view_func=views.task_page, methods=["GET","POST"])
    app.add_url_rule("/reminder", view_func=views.reminder_page, methods=["GET","POST"])
    app.add_url_rule("/groups", view_func=views.group_page, methods=["GET","POST"])
    app.add_url_rule("/group_create", view_func=views.group_create_page, methods=["GET","POST"])
    app.add_url_rule("/group_tasks", view_func=views.group_tasks_page, methods=["GET","POST"])
    app.add_url_rule("/group_reminders", view_func=views.group_reminders_page, methods=["GET","POST"])
    app.add_url_rule("/group_update", view_func=views.group_update_page, methods=["GET","POST"])
    app.add_url_rule("/edit_profile", view_func=views.edit_profile_page, methods=["GET","POST"])
    app.add_url_rule("/getReminders", view_func=views.getReminders, methods=["GET","POST"])
    app.add_url_rule("/getGroupReminders", view_func=views.getGroupReminders, methods=["GET","POST"])
    app.add_url_rule("/getTasks", view_func=views.getTasks, methods=["GET","POST"])
    app.add_url_rule("/getGroupTasks", view_func=views.getGroupTasks, methods=["GET","POST"])
    app.add_url_rule("/searchTasks", view_func=views.searchTasks, methods=["GET","POST"])
    app.add_url_rule("/searchGroupTasks", view_func=views.searchGroupTasks, methods=["GET","POST"])
    app.add_url_rule("/searchReminders", view_func=views.searchReminders, methods=["GET","POST"])
    app.add_url_rule("/searchGroupReminders", view_func=views.searchGroupReminders, methods=["GET","POST"])
    app.add_url_rule("/deleteUserAlert", view_func=views.deleteUserAlert, methods=["GET","POST"])
    app.add_url_rule("/deleteGroupAlert", view_func=views.deleteGroupAlert, methods=["GET","POST"])
    app.add_url_rule("/updateUserAlert", view_func=views.updateUserAlert, methods=["GET","POST"])
    app.add_url_rule("/updateGroupAlert", view_func=views.updateGroupAlert, methods=["GET","POST"])
    app.add_url_rule("/upcomingTasks", view_func=views.upcomingTasks, methods=["GET","POST"])
    app.add_url_rule("/upcomingGroupTasks", view_func=views.upcomingGroupTasks, methods=["GET","POST"])
    app.add_url_rule("/getUser", view_func=views.getUser, methods=["GET","POST"])
    app.add_url_rule("/getAdminGroup", view_func=views.getAdminGroup, methods=["GET","POST"])
    app.add_url_rule("/nonAdminGroup", view_func=views.nonAdminGroup, methods=["GET","POST"])
    return app


app = create_app()



if __name__ == "__main__": 
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '2021'))
    except ValueError:
        PORT = 2021
    app.run(HOST, PORT,debug=True)

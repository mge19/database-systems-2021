import os
import psycopg2 as dbapi2
import datetime

def execute_sql(command):
    print("executing...")
    print(command)
    try:
            url="postgres://mkstwwsqziogdt:821d366826d60dd49017e47a785b3c588d3bc3d847fd7fc18f6b9fe85abd0d9e@ec2-54-247-158-179.eu-west-1.compute.amazonaws.com:5432/dfl517spu7ensr"
            #url="postgres://postgres:1a2b3c@localhost:5432/postgres"  
            print("debug0")
            connection = dbapi2.connect(url)
            print("debug1")
            cursor = connection.cursor()
            print("debug2")
            cursor.execute(command)
            print("Execute works!!")

            connection.commit()

    except dbapi2.DatabaseError:
            print("dataerror2")
            print(dbapi2.DatabaseError)
            connection.rollback()
            return -1;

    try:
            data_column = []
            data_content = cursor.fetchall()
            #print(data_content)
            if (data_content == [] or data_content == [[]]):
               print("data bos")
               return -2
            data_column.append(tuple([desc[0] for desc in cursor.description]))
            data_column += data_content
            cursor.close()
            connection.close()

    except dbapi2.DatabaseError:
            print("dataerror3")
            print(dbapi2.DatabaseError)
            connection.rollback()
            return -3

    return data_column

def get_all_users(): #get email using user id
    command = """SELECT * FROM USERS;"""
    data = execute_sql(command)
    return data

def get_user_id(email): #check if email and password pair in database
    command = """SELECT user_id FROM USERS 
                WHERE email = '%(email)s';"""
    data = execute_sql(command % {'email': email})
    if (data == -2): #empty result
        return -1
    return data
  
def check_password(email, password): #check if email and password pair in database
    command = """SELECT user_id FROM USERS 
                WHERE email = '%(email)s' AND password = '%(password)s';"""
    data = execute_sql(command % {'email': email, 'password': password})
    if (data == -2): #empty result
        return -1
    return data

def get_user_info(user_id): #get email using user id
    command = """SELECT * FROM USERS 
                WHERE user_id = '%(user_id)s';"""
    data = execute_sql(command % {'user_id': user_id})
    return data

  
def get_user_password(email): #get email using user id
    command = """SELECT password FROM USERS 
                WHERE email = '%(email)s';"""
    data = execute_sql(command % {'email': email})
    if (data == -2): #empty result
        return -1
    return data
  
def update_user_password(user_id, password): #get email using user id
    command = """UPDATE USERS 
                SET password = '%(password)s'
                WHERE user_id = '%(user_id)s';"""
    data = execute_sql(command % {'user_id': user_id, 'password': password})
    return data

def update_user_first_name(user_id, first_name): #get email using user id
    command = """UPDATE USERS 
                SET first_name = '%(first_name)s'
                WHERE user_id = '%(user_id)s';"""
    data = execute_sql(command % {'user_id': user_id, 'first_name': first_name})
    return data

def update_user_last_name(user_id, last_name): #get email using user id
    command = """UPDATE USERS 
                SET last_name = '%(last_name)s'
                WHERE user_id = '%(user_id)s';"""
    data = execute_sql(command % {'user_id': user_id, 'last_name': last_name})
    return data

def update_user_email(user_id, email): #get email using user id
    command = """UPDATE USERS 
                SET email = '%(email)s'
                WHERE user_id = '%(user_id)s';"""
    data = execute_sql(command % {'user_id': user_id, 'email': email})
    return data
def delete_user(user_id):
    command = """DELETE FROM GROUPS_USERS
                 WHERE user_id='%(user_id)s';"""
    data = execute_sql(command % {'user_id': user_id})
    command = """DELETE FROM USER_ALERTS
                 WHERE user_id='%(user_id)s';"""
    data = execute_sql(command % {'user_id': user_id})
    command = """DELETE FROM USERS
                 WHERE user_id='%(user_id)s';"""
    data = execute_sql(command % {'user_id': user_id})
def get_user_groups(user_id):
    command = """SELECT * FROM GROUPS_USERS INNER JOIN GROUPS
                ON GROUPS_USERS.user_id = GROUPS.user_id
                WHERE user_id = '%(user_id)s';"""
    data = execute_sql(command % {'user_id': user_id})
    return data


def get_user_reminders(user_id): #If group_name == user_id then this group only contains one user
    command = """SELECT alert_id, alert_time, title, message, urgency
                FROM USER_ALERTS
                WHERE user_id = '%(user_id)s' AND type = 'reminder';"""
    data = execute_sql(command % {'user_id': user_id})
    return data


def get_user_tasks(user_id):
    command = """SELECT alert_id, alert_time, title, message, urgency
                FROM USER_ALERTS
                WHERE user_id = '%(user_id)s' AND type = 'task';"""
    data = execute_sql(command % {'user_id': user_id})
    return data

def get_group_reminders(group_id):
    command = """SELECT alert_id, alert_time, title, message, urgency
                FROM GROUP_ALERTS
                WHERE group_id = '%(group_id)s' AND type = 'reminder';"""
    data = execute_sql(command % {'group_id' : group_id})
    return data

def get_group_tasks(group_id):
    command = """SELECT alert_id, alert_time, title, message, urgency
                FROM GROUP_ALERTS 
                WHERE group_id = '%(group_id)s' AND type = 'task';"""
    data = execute_sql(command % {'group_id' : group_id})
    return data

def add_user(first_name, last_name, email, password):
    command = """INSERT INTO USERS (first_name, last_name, email, password)
                 VALUES ('%(first_name)s',
                         '%(last_name)s',
                         '%(email)s',
                         '%(password)s');"""
    return execute_sql(command % {'first_name': first_name,'last_name': last_name, 'email': email, 'password': password})

def add_user_task(user_id, alert_time, title, message, urgency):
    command = """INSERT INTO USER_ALERTS (user_id, alert_time, title, message, urgency, type)
                 VALUES ('%(user_id)s',
                         '%(alert_time)s',
                         '%(title)s',
                         '%(message)s',
                         '%(urgency)s',
                         'task');""";
    return execute_sql(command % {'user_id': user_id, 'alert_time': alert_time, 'title': title, 'message': message, 'urgency': urgency})

def add_user_reminder(user_id, alert_time, title, message, urgency):
    command = """INSERT INTO USER_ALERTS (user_id, alert_time, title, message, urgency, type)
                 VALUES ('%(user_id)s',
                         '%(alert_time)s',
                         '%(title)s',
                         '%(message)s',
                         '%(urgency)s',
                         'reminder');""";
    return execute_sql(command % {'user_id': user_id, 'alert_time': alert_time, 'title': title, 'message': message, 'urgency': urgency})

def update_user_alert(alert_id, alert_time, title, message, urgency):
    command = """UPDATE USER_ALERTS
                 SET alert_time='%(alert_time)s',
                 title='%(title)s',
                 message='%(message)s',
                 urgency='%(urgency)s'
                 WHERE alert_id='%(alert_id)s';"""
    return execute_sql(command % {'alert_id' : alert_id ,'alert_time': alert_time, 'title': title, 'message': message, 'urgency': urgency})

def add_group_task(group_id, alert_time, title, message, urgency):
    command = """INSERT INTO GROUP_ALERTS (group_id, alert_time, title, message, urgency, type)
                 VALUES ('%(group_id)s',
                         '%(alert_time)s',
                         '%(title)s',
                         '%(message)s',
                         '%(urgency)s',
                         'task');"""
    return execute_sql(command % {'group_id': group_id, 'alert_time': alert_time, 'title': title, 'message': message, 'urgency': urgency})

def add_group_reminder(group_id, alert_time, title, message, urgency):
    command = """INSERT INTO GROUP_ALERTS (group_id, alert_time, title, message, urgency, type)
                 VALUES ('%(group_id)s',
                         '%(alert_time)s',
                         '%(title)s',
                         '%(message)s',
                         '%(urgency)s',
                         'reminder');"""
    return execute_sql(command % {'group_id': group_id, 'alert_time': alert_time, 'title': title, 'message': message, 'urgency': urgency})

def update_group_alert(alert_id, alert_time, title, message, urgency):
    command = """UPDATE GROUP_ALERTS
                 SET alert_time='%(alert_time)s',
                 title='%(title)s',
                 message='%(message)s',
                 urgency='%(urgency)s'
                 WHERE alert_id='%(alert_id)s';"""
    return execute_sql(command % {'alert_id' : alert_id ,'alert_time': alert_time, 'title': title, 'message': message, 'urgency': urgency})

def delete_user_alert(alert_id):
    command = """DELETE FROM USER_ALERTS
                 WHERE alert_id = '%(alert_id)s';"""
    print(command)
    data = execute_sql(command % {'alert_id': alert_id})
    return data
    
def delete_group_alert(alert_id):
    command = """DELETE FROM GROUP_ALERTS
                 WHERE alert_id = '%(alert_id)s';"""

    data = execute_sql(command % {'alert_id': alert_id})
    return data

def delete_group(group_id):
    command = """DELETE FROM GROUPS_USERS
                 WHERE group_id = '%(group_id)s';"""
    data = execute_sql(command % {'group_id': group_id})
    
    command = """DELETE FROM GROUP_ALERTS
                 WHERE group_id = '%(group_id)s';"""

    data = execute_sql(command % {'group_id': group_id})
    command = """DELETE FROM GROUPS
                 WHERE group_id = '%(group_id)s';"""

    data = execute_sql(command % {'group_id': group_id})
    
    return data

def leave_group(user_id,group_id):
    command = """DELETE FROM GROUPS_USERS
                 WHERE user_id = '%(user_id)s'AND group_id = '%(group_id)s';"""

    data = execute_sql(command % {'user_id': user_id,'group_id': group_id})
    return data    

def update_group(group_id,new_group_name,new_description,admins,users):
    command = """DELETE FROM GROUPS_USERS
                 WHERE group_id = '%(group_id)s';"""
    data = execute_sql(command % {'group_id': group_id})
    command = """UPDATE GROUPS 
                SET group_name = '%(new_group_name)s' ,
                description = '%(new_description)s' 
                WHERE group_id = '%(group_id)s';"""
    data = execute_sql(command % {'group_id': group_id, 'new_group_name': new_group_name,'new_description':new_description})
    for admin in admins:
        command=add_user_to_group(admin,group_id,'y')
    print("Admins are added to groups_users table")
    for user in users:
        command=add_user_to_group(user,group_id,'n')
    print("Other users are added to groups_users table")
    return

def search_user_reminder_date(user_id, date_time,type):
    datetime1=date_time
    if(type==0):
        datetime1=datetime1.replace(year=datetime1.year+1)
    elif(type==1):
        if date_time.month==12:
            datetime1=datetime1.replace(year=datetime1.year+1,month=1)
        else:    
            datetime1=datetime1.replace(month=datetime1.month+1)
    elif(type==2):
        datetime1=datetime1+datetime.timedelta(days=1)
    command = """
    SELECT * FROM USER_ALERTS
    WHERE alert_time >= '%(datetime)s' AND alert_time < '%(datetime1)s' AND user_id = '%(user_id)s' AND type = 'reminder';"""
    data = execute_sql(command % {'datetime' : date_time,'datetime1' : datetime1,'user_id': user_id})
    return data

def search_user_task_date(user_id, date_time,type):
    datetime1=date_time
    if(type==0):
        datetime1=datetime1.replace(year=datetime1.year+1)
    elif(type==1):
        if date_time.month==12:
            datetime1=datetime1.replace(year=datetime1.year+1,month=1)
        else:    
            datetime1=datetime1.replace(month=datetime1.month+1)
    elif(type==2):
        datetime1=datetime1+datetime.timedelta(days=1)
    command = """
    SELECT * FROM USER_ALERTS
    WHERE alert_time >= '%(datetime)s' AND alert_time < '%(datetime1)s' AND user_id = '%(user_id)s' AND type = 'task';"""
    data = execute_sql(command % {'datetime' : date_time,'datetime1' : datetime1,'user_id': user_id})
    return data

def search_group_reminder_date(group_id, date_time,type):
    datetime1=date_time
    if(type==0):
        datetime1=datetime1.replace(year=datetime1.year+1)
    elif(type==1):
        if date_time.month==12:
            datetime1=datetime1.replace(year=datetime1.year+1,month=1)
        else:    
            datetime1=datetime1.replace(month=datetime1.month+1)
    elif(type==2):
        ddatetime1=datetime1+datetime.timedelta(days=1)
    command = """
    SELECT * FROM GROUP_ALERTS
    WHERE alert_time >= '%(datetime)s' AND alert_time < '%(datetime1)s' AND group_id = '%(group_id)s' AND type = 'reminder';"""
    data = execute_sql(command % {'datetime' : date_time,'datetime1' : datetime1,'group_id': group_id})
    return data

def search_group_task_date(group_id, date_time,type):
    datetime1=date_time
    if(type==0):
        datetime1=datetime1.replace(year=datetime1.year+1)
    elif(type==1):
        if date_time.month==12:
            datetime1=datetime1.replace(year=datetime1.year+1,month=1)
        else:    
            datetime1=datetime1.replace(month=datetime1.month+1)
    elif(type==2):
        datetime1=datetime1+datetime.timedelta(days=1)
    command = """
    SELECT * FROM GROUP_ALERTS
    WHERE alert_time >= '%(datetime)s' AND alert_time < '%(datetime1)s' AND group_id = '%(group_id)s' AND type = 'task';"""
    data = execute_sql(command % {'datetime' : date_time,'datetime1' : datetime1,'group_id': group_id})
    return data

def search_user_reminder_title(user_id, title):
    command = """
    SELECT * FROM USER_ALERTS
    WHERE STRPOS(title,'%(title)s')>0 AND user_id = '%(user_id)s' AND type = 'reminder';"""
    data = execute_sql(command % {'title' : title,'user_id': user_id})
    return data

def search_user_task_title(user_id, title):
    command = """
    SELECT * FROM USER_ALERTS
    WHERE STRPOS(title,'%(title)s')>0 AND user_id = '%(user_id)s' AND type = 'task';"""
    data = execute_sql(command % {'title' : title,'user_id': user_id})
    return data
    
def search_group_reminder_title(group_id, title):
    command = """
    SELECT * FROM GROUP_ALERTS
    WHERE STRPOS(title,'%(title)s')>0 AND group_id = '%(group_id)s' AND type = 'reminder';"""
    data = execute_sql(command % {'title' : title,'group_id': group_id})
    return data

def search_group_task_title(group_id, title):
    command = """
    SELECT * FROM GROUP_ALERTS
    WHERE STRPOS(title,'%(title)s')>0 AND group_id = '%(group_id)s' AND type = 'task';"""
    data = execute_sql(command % {'title' : title,'group_id': group_id})
    return data

def get_user_groups(user_id):
    command = """
    SELECT * FROM GROUPS_USERS
    WHERE user_id = '%(user_id)s';"""
    data = execute_sql(command % {'user_id': user_id})
    return data

def get_user_admin_groups(user_id):
    command = """SELECT * FROM GROUPS_USERS INNER JOIN GROUPS
                ON GROUPS_USERS.group_id = GROUPS.group_id
                WHERE user_id = '%(user_id)s'  AND admin = 'y';"""
    data = execute_sql(command % {'user_id': user_id})
    print(data)
    return data

def get_user_nonadmin_groups(user_id):
    command = """SELECT * FROM GROUPS_USERS INNER JOIN GROUPS
                ON GROUPS_USERS.group_id = GROUPS.group_id
                WHERE user_id = '%(user_id)s'  AND admin = 'n';"""
    data = execute_sql(command % {'user_id': user_id})
    return data

def join_group(user_id, group_name):
    command = """SELECT group_id from GROUPS
        WHERE group_name='%(group_name)s';"""
    data = execute_sql(command % {'group_name': group_name})
    print(data)
    if data!=-2:
        group_id=data[1][0]
        command = """SELECT * FROM GROUPS_USERS
        WHERE group_id='%(user_id)s' AND user_id='%(user_id)s'"""
        data = execute_sql(command % {'user_id': user_id, 'group_id': group_id})
        if data==-2:
            command = """
            INSERT INTO GROUPS_USERS (user_id, group_id, admin)
            VALUES ('%(user_id)s',
                    '%(group_id)s',
                    'n');"""
            
            return execute_sql(command % {'user_id': user_id, 'group_id': group_id})
        else:
            return '1'
    else:
        return '0'
def create_group(group_name, description, admins, users):
    command = """
    INSERT INTO GROUPS (group_name, description)
    VALUES ('%(group_name)s',
            '%(description)s');"""
    execute_sql(command % {'group_name': group_name, 'description': description})

    print("group is created")

    command = """
    SELECT group_id FROM GROUPS 
    WHERE group_name = '%(group_name)s';"""

    group_id = execute_sql(command % {'group_name': group_name, 'description': description})[1][0]

    print("group_id of the group created is taken from db")
    for admin in admins:
        command=add_user_to_group(admin,group_id,'y')

    print("Admins are added to groups_users table")
    for user in users:
        command=add_user_to_group(user,group_id,'n')

    print("Other users are added to groups_users table")
    return 
def add_user_to_group(user_id, group_id,admin):
    command = """
    INSERT INTO GROUPS_USERS (user_id, group_id, admin)
    VALUES ('%(user_id)s',
            '%(group_id)s',
            '%(admin)s');"""
    return execute_sql(command % {'user_id': user_id, 'group_id': group_id,'admin': admin})

def get_upcoming_user_tasks(user_id):
    d = datetime.datetime.now()
    days_ahead = 7
    weekday = d + datetime.timedelta(days_ahead)    
    command="""SELECT * FROM USER_ALERTS
    WHERE alert_time >= '%(datetime1)s' AND alert_time < '%(datetime2)s' AND user_id = '%(user_id)s' AND type = 'task';"""
    data = execute_sql(command % {'datetime1' : d,'datetime2' : weekday,'user_id': user_id})
    return data

def get_upcoming_group_tasks(group_id):
    d = datetime.datetime.now()
    days_ahead = 7
    weekday = d + datetime.timedelta(days_ahead)    
    command="""SELECT * FROM GROUP_ALERTS
    WHERE alert_time >= '%(datetime1)s' AND alert_time < '%(datetime2)s' AND group_id = '%(group_id)s' AND type = 'task';"""
    data = execute_sql(command % {'datetime1' : d,'datetime2' : weekday,'group_id': group_id})
    return data

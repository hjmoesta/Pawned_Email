import sqlite3
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from tester.forms import SignUpForm
from tester.keys import api_key
import requests
from json import JSONDecodeError

def signin(request,prompt="Please enter email and password"):
    return render(request,'signin.html',{'prompt': prompt})


def signup(request,prompt="Please Provide an Email"):
    return render(request, 'signup.html', {'prompt': prompt})

def signup_success(request):
    email= request.POST.get("email")
    password= request.POST.get("password")
    conn = sqlite3.connect('web_login.db')
    if not check_if_user_exists(conn, email):
        store_values(conn,email,password)
        try:
            pwnd_name=[]
            pwnd_data = call_api(email)
            for breach in pwnd_data:
                pwnd_name.append(breach['Name'])
            add_api_data_to_db(conn, pwnd_data, email.split('@')[0])
            return render(request,'content_signup.html', {'data': pwnd_name , 'email': email})
        except (JSONDecodeError):
            prompt = "There are no breaches on your email"
            return render(request, 'signup.html', {'prompt': prompt})
    else:
        prompt = "This email is already being used. Try another or login"
        return render(request, 'signup.html', {'prompt': prompt})

def signin_success(request):
    email= request.POST.get("email")
    password= request.POST.get("password")
    conn = sqlite3.connect('web_login.db')
    if check_if_user_exists(conn,email):
        valid_bool,prompt = check_user(conn,email,password)
        if valid_bool:
            try:
                pwnd_data = get_api_data_from_db(conn, email.split('@')[0])
                return render(request,'content_signin.html', {'data': pwnd_data , 'email': email})
            except ():
                prompt = "There was an error that occured"
                return render(request,'signin.html',{'prompt': prompt})
        else:
            prompt = "Invalid password"
            return render(request,'signin.html',{'prompt': prompt})
    else:
        prompt = "This email is not being used. Try another or signup"
        return render(request, 'signin.html', {'prompt': prompt})




########DATABASE FUNCTIONS###########

def store_values(conn, email, password):
    cur = conn.cursor()
    sql = '''INSERT INTO users(email,password) VALUES(?,?)'''
    cur.execute(sql,(email,password))
    conn.commit()

def check_user(conn, email, password):
    cur = conn.cursor()
    sql_email_statement = '''SELECT * FROM users'''
    for sql_obj in cur.execute(sql_email_statement):
        if sql_obj[0] == email and sql_obj[1] == password:
            return (True,"")
    return (False,"Email was not found")

def check_if_user_exists(conn, email):
    cur = conn.cursor()
    sql_email = '''SELECT email FROM users '''
    for sql_email in cur.execute(sql_email):
        if email == sql_email[0]:
            return True
    return False

def add_api_data_to_db(conn, data, email):
    cur = conn.cursor()
    sql_stmt = '''
CREATE TABLE {} (
    breach_name TEXT
);'''.format(email)
    cur.execute(sql_stmt)
    for name in data:
        sql_add_name = '''INSERT INTO {}(breach_name) VALUES(?);'''.format(email)
        cur.execute(sql_add_name,(name['Name'],))
    conn.commit()

def get_api_data_from_db(conn, email):
    cur = conn.cursor()
    sql_stmt = '''SELECT breach_name FROM {};'''.format(email)
    return cur.execute(sql_stmt)

##################################################################################

def call_api(email):
    headers= {'hibp-api-key': api_key}
    url = 'https://haveibeenpwned.com/api/v3/breachedaccount/{data}'.format(data=email)
    response = requests.get(url, headers=headers)
    pwnd_data = response.json()
    return pwnd_data



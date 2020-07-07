import tkinter
import mysql.connector
from PIL import Image
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, json, jsonify


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.secret_key = "super secret key"                         #security for encrption code

def getDb():
    mydb = mysql.connector.connect(
        host="localhost",
        user="latika",
        passwd="Latika@123",
        database="steganography")
    return mydb


@app.route('/')                               # home page
def home():
    session.pop('username', None)
    session.pop('password', None)
    return render_template("login.html")


@app.route('/login', methods=['POST', 'GET'])  # login validation for login page
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        db = getDb()
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM users WHERE username LIKE %s AND password LIKE %s", (username, password))
        total = mycursor.rowcount
        for x in mycursor:
            if username and password:
                    return redirect(url_for('dashboard'))
            else:
                msg = "Invalid entry"
                return render_template("login.html", details=msg)
    msg = "Invalid email and password"
    return render_template("login.html", details=msg)

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    username = session.get('username')
    if username is not None:
        db = getDb()
        cursor = db.cursor()
        cursor.execute("select username,imagepath from images where username= '"+ username+ "' ")
        fetching_size = 30
        res = cursor.fetchmany(fetching_size)
        details = []
        for x in res:
            details.append({"username": x[0], "images": x[1]})

        return render_template("dashboard.html",details=details)
    else:
        return render_template("login.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
        return render_template("register.html")

@app.route('/registration_check', methods=['POST', 'GET'])
def registration_check():
    if request.method == 'POST':
        name = request.form['username_new']
        password = request.form['password_new']
        try :
            db = getDb()
            mycursor = db.cursor(buffered=True)
            mycursor.execute("insert into users(username,password)values('" + name + "','" + password + "')")
            db.commit()
            mycursor.close()
        except:
            flash('Username already exist')
            msg = "Username already exist"
            return render_template("register.html", details=msg)

    msg = "Successfully Registered"
    return render_template("login.html", details=msg)

@app.route('/encrypt', methods=['POST', 'GET'])
def encrypt():
        return render_template("encrypt.html")

@app.route('/encrypt_form', methods=['POST', 'GET'])
def encrypt_form():
    # return render_template("dashboard.html")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run()
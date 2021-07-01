import re
from flask import Flask, render_template, url_for, redirect, request, session
import mysql
from flask_mysqldb import MySQL
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=1)
#connecting to database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'grocery'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
@app.route('/')
def home():
    cur = mysql.connection.cursor()
    sql_query = 'SELECT * FROM products'
    cur.execute(sql_query)
    students = cur.fetchall()
    cur.close()
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/bread')
def bread():
    return render_template('bread.html')

@app.route('/drinks')
def drinks():
    return render_template('drinks.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/frozen')
def frozen():
    return render_template('frozen.html')

@app.route('/household')
def household():
    return render_template('household.html')

@app.route('/kitchen')
def kitchen():
    return render_template('kitchen.html')

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        signinusername, signinpassword = request.form.get('signinusername',''), request.form.get('signinpassword','')
        signupusername, signupemail, signuppassword = request.form.get('signupusername',''), request.form.get('signupemail',''), request.form.get('signuppassword','')
        if signinpassword and signinusername:
            cur = mysql.connection.cursor()
            sql_query = 'SELECT Username,Password FROM login_details;'
            cur.execute(sql_query)
            data = list(cur.fetchall())
            cur.close()
            session['username'], session['password'], session['logincheck'] = signinusername, signinpassword, None
            session.permanent = True
            for person in data:
                if person['Username'] == session['username'] and person['Password'] == session['password']:
                    session['loggedin'] = True
                    return redirect(url_for('home'))
            session['logincheck'] = "Invalid username or password"
            return redirect(url_for('login'))
        elif signupusername and signupemail and signuppassword:
            session['username'], session['password'], session['email'], session['logincheck'] = signupusername, signuppassword, signupemail, None
            session.permanent = True
            cur = mysql.connection.cursor()
            sql_query = 'SELECT * FROM login_details WHERE Email = "{}"'.format(signupemail)
            cur.execute(sql_query)
            personexists = list(cur.fetchall())
            cur.close()
            if len(personexists)>0:
                session['logincheck'] = "User already exists Please login"
                return redirect(url_for('login'))
            else:
                cur = mysql.connection.cursor()
                sql_query = 'INSERT INTO login_details (Username, Email, Password) VALUES ("{}", "{}", "{}");'.format(signupusername, signupemail, signuppassword)
                cur.execute(sql_query)
                mysql.connection.commit()
                cur.close()
                session['loggedin'] = True
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('grocery-login.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))
@app.route('/ouraid')
def ouraid():
    return render_template('ouraid.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/single')
def single():
    return render_template('single.html')

@app.route('/vegetables')
def vegetables():
    return render_template('vegetables.html')

if __name__=='__main__':
    app.run(debug=True)

'''w3l->grocery,w3agile->grocery'''
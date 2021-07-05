# Libraries
import re
from flask import Flask, render_template, url_for, redirect, request, session
from flask_mysqldb import MySQL
from datetime import timedelta
# Initialization
app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=1)
# connecting to database
app.config['MYSQL_HOST'] = 'brk5hkdoqxwzb4pymez6-mysql.services.clever-cloud.com'
app.config['MYSQL_DB'] = 'brk5hkdoqxwzb4pymez6'
app.config['MYSQL_USER'] = 'uzacqdcathxgavtv'
app.config['MYSQL_PASSWORD'] = '18VXcPSB2cPTFz2G0CY2'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


def execute_query(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    if query[0] == 'S':
        data = list(cur.fetchall())
    else:
        mysql.connection.commit()
        return
    cur.close()
    return data

@app.route('/test')
def test():
    return render_template('test.html')
@app.route('/upload',methods=['POST'])
def upload():
    image = request.files['image']
    if image:
       image = r"C:\Users\makin\Desktop\GroceryManagementSystem\static\images\{}".format(image.filename)
       with open(image, 'rb') as file:
           bindata = file.read()
       execute_query('INSERT INTO test (Photo) VALUES("{}");'.format(tuple(bindata)))
       return redirect(url_for('load'))
    return "notdone"

@app.route('/load')
def load():
    data = execute_query('SELECT Photo FROM test')
    
    return "done"

@app.route('/')
def home():
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
            data = execute_query('SELECT Username,Password FROM login_details;')
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
            personexists = execute_query('SELECT * FROM login_details WHERE Email = "{}"'.format(signupemail))
            if len(personexists)>0:
                session['logincheck'] = "User already exists Please login"
                return redirect(url_for('login'))
            else:
                execute_query('INSERT INTO login_details (Username, Email, Password) VALUES ("{}", "{}", "{}");'.format(signupusername, signupemail, signuppassword))
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

'w3l->grocery,w3agile->grocery'
# Libraries
import re
import random
from flask import Flask, render_template, url_for, redirect, request, session
from flask_paginate import Pagination, get_page_args
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from datetime import timedelta
# Initialization
app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=30)
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
    data = execute_query('SELECT * FROM product_details WHERE product_id = "{}" OR product_id = "{}" OR product_id = "{}" OR product_id = "{}"'.format("PRFR004","PRKI010","PRVE008","PRFZ012"))
    session['admin'] = False
    return render_template('home.html',data = data, n = len(data))

@app.route('/search/<searchname>', methods=["POST","GET"])
def search(searchname):
    if request.method=='POST' or searchname != 'default':
        if searchname == 'default':
            searched_name = request.form.get('searched_name','')
            return redirect(url_for('search',searchname = searched_name))
        else:
            searchname = searchname.lower().split()
            products = execute_query('SELECT product_id,LOWER(product_name) AS product_name FROM product_details')
            mylist = [ [product['product_id'],list(product['product_name'].split())] for product in products]
            print(mylist)
            return "<h1> product will be searched</h1>"
    else:
        return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
@app.route('/admin/<text>', methods = ['POST','GET'])
def admin(text = None):
    if not session.get('admin',False):
        return """<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
                <body style="backgorund-color:red"><div class="container"><h1 style = "text-align:center;padding-top:100px;">You are not administrator</h1>
                <img src="https://images-na.ssl-images-amazon.com/images/I/71QIwIAtQGL._SL1500_.jpg" alt="Restricted Area" srcset="" style="display:block;margin-left:auto;margin-right:auto;width:50%">
                <a href = "{}" style = "text-align:center;text-decoration:none;display:block;">Return back</a></div></body>
                """.format(url_for('home'))
    else:
        if text == "PRODUCTEDITED":
            product_id, product_name, product_price, prodict_with_discount, discount, description, instock, product_units = request.form.get('editproductid',''), request.form.get('editproductname',''), request.form.get('editproductprice',''), request.form.get('editproductwithdiscount',''), request.form.get('editdiscount',''), request.form.get('editproductdescription',''), request.form.get('editproductinstock',''), request.form.get('editproductunits','')
            
            pass
        elif text == "PRODUCTDELETED":
            pass
        elif text == "PRODUCTEDADDED":
            pass
        products = execute_query('SELECT * FROM product_details')
        page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
        total = len(products)
        pagination_users = products[offset:offset+per_page]
        pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
        return render_template('admin.html',products=pagination_users,page=page,per_page=per_page,pagination=pagination,)


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
            if signinusername == "ADMIN" and signinpassword == "admin132001@gmail.com":
                session['admin'],session['loggedin'] = True, True
                return redirect(url_for('admin'))
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
    fruits = execute_query('SELECT * FROM product_details WHERE product_id LIKE "PRFR___" LIMIT 4')
    vegetables = execute_query('SELECT * FROM product_details WHERE product_id LIKE "PRVE___" LIMIT 4')
    drinks = execute_query('SELECT * FROM product_details WHERE product_id LIKE "PRDR___" LIMIT 4')
    return render_template('products.html', fruits = fruits,vegetables = vegetables,drinks = drinks, n=4)

@app.route('/single/<product_id>')
def single(product_id):
    ids = ['PRFR___','PRVE___','PRKI___','PRDR___','PRBR___','PRFZ___']
    item = execute_query('SELECT * FROM product_details WHERE product_id = "{}"'.format(product_id))
    related = execute_query('SELECT * FROM product_details WHERE product_id <> "{}" AND product_id LIKE "{}" LIMIT 4'.format(product_id,product_id[:4]+"___"))
    choices = list(filter(lambda x : x != product_id[:4]+"___", ids))
    choice1 = execute_query('SELECT * FROM product_details WHERE product_id LIKE "{}" LIMIT 4'.format(random.choice(choices))) 
    choice2 = execute_query('SELECT * FROM product_details WHERE product_id LIKE "{}" LIMIT 4'.format(random.choice(choices)))
    while choice1 == choice2:
        choice2 = execute_query('SELECT * FROM product_details WHERE product_id LIKE "{}" LIMIT 4'.format(random.choice(choices)))
    return render_template('single.html', item = item[0], related = related, choice1 = choice1, choice2 = choice2)

@app.route('/vegetables')
def vegetables():
    vegetables = execute_query('SELECT * FROM product_details WHERE product_id LIKE "PRVE___"')
    return render_template('vegetables.html',vegetables1 = vegetables[:4], vegetables2 = vegetables[4:8], vegetables3 = vegetables[8:12])

if __name__=='__main__':
    app.run(debug=True)

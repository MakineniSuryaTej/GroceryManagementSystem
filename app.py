from flask import Flask,render_template,url_for

app = Flask(__name__)

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

@app.route('/login')
def login():
    return render_template('grocery-login.html')

@app.route('/ouraid')
def ouraid():
    return render_template('ouraid.html')

@app.route('/products')
def products():
    return render_template('products.html')

if __name__=='__main__':
    app.run(debug=True)
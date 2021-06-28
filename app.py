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

@app.route('/frozen')
def frozen():
    return render_template('frozen.html')

@app.route('/household')
def household():
    return render_template('household.html')

@app.route('/kitchen')
def kitchen():
    return render_template('kitchen.html')

@app.route('/login')
def login():
    return render_template('grocery-login.html')

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
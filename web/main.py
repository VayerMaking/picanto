# flask server
from tinydb import TinyDB, Query
from datetime import datetime
from flask import Flask, render_template, request
 
app = Flask(__name__) 
db = TinyDB("db.json")
Order = Query()
 
@app.route('/orders', methods=['POST'])
def makeOrder():
    order = request.get_json()
    db.insert(order)
    return 'ok'

@app.route('/orders', methods=['GET'])
def getOrders():
    orders = db.all()
    return orders

def removeFinishedOrders():
    db.remove(Order.status == 'completed')
    return "ok"

# @app.route("/") 
# def index(): 
#     return render_template('index.html')

@app.route("/oven_start", methods=['POST'])
def oven_start():
    db.update({'status': 'in the oven'}, Order.status == 'preparation')
    return "ok"

@app.route("/tracker", methods=['GET'])
def tracker(): 
    return render_template('kitchen.html')

@app.route("/cashier", methods=['GET']) 
def cashier(): 
    return render_template('pizza.html')

@app.route("/take_order", methods=['GET']) 
def take_order(): 
    return render_template('pizza2.html')

@app.route("/overview", methods=['GET']) 
def cashier(): 
    return render_template('order_overview.html')
 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
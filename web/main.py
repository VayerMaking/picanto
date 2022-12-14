# flask server
import random
import string
from tinydb import TinyDB, Query
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import requests
import threading
import time
 
app = Flask(__name__) 
db = TinyDB("db.json")
Order = Query()
 
@app.route('/orders', methods=['POST'])
def makeOrder():
    order = request.get_json()
    order['id'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    order['time_start'] = None
    db.insert(order)
    return jsonify("ok")

@app.route('/orders', methods=['GET'])
def getOrders():
    orders = db.all()
    return orders

def removeFinishedOrders():
    db.remove(Order.status == 'Completed')
    return "ok"

# @app.route("/") 
# def index(): 
#     return render_template('index.html')

@app.route("/oven_start", methods=['POST'])
def oven_start():
    last_order = db.get(doc_id=1)
    if last_order['status'] == 'Preparing':
        print("timestamp: ", request.get_json()['timestamp'], flush=True)
        db.update({'status': 'In the oven', 'time_start' : request.get_json()['timestamp']}, Query().id == last_order['id'])
        db.update({'time_start' : request.json()['timestamp']}, Query['id'] == last_order['id'])
    return "ok"

@app.route("/tracker", methods=['GET'])
def tracker(): 
    orders = requests.get('http://127.0.0.1:8080/orders').json()
    print(orders)
    return render_template('kitchen.html', orders=orders)

@app.route("/cashier", methods=['GET']) 
def cashier(): 
    return render_template('pizza.html')

@app.route("/take_order", methods=['GET']) 
def take_order(): 
    return render_template('pizza2.html')

@app.route("/overview", methods=['GET']) 
def overview(): 
    return render_template('order_overview.html')
 
def start_server():
    app.run(host="0.0.0.0", port=8080, use_reloader=False)

def timer():
    while True:
        orders = db.all()
        for order in orders:
            if order['status'] == 'In the oven':
                elapsed = datetime.now() - datetime.strptime(order['time_start'], '%H:%M:%S')
                print("time elapsed: ", elapsed.seconds / 60, flush=True)
                if elapsed.seconds / 60 > 1:
                    db.update({'status': 'Ready'}, Order.id == order['id'])
            if order['status'] == 'Ready':
                elapsed = datetime.now() - datetime.strptime(order['time_start'], '%H:%M:%S')
                print("time elapsed: ", elapsed.seconds / 60, flush=True)
                if elapsed.seconds / 60 > 2:
                    db.remove(Order.id == order['id'])
        time.sleep(10)

if __name__=='__main__':
    stateThread = threading.Thread(target=timer)
    stateThread.daemon = True
    stateThread.start()
    webThread = threading.Thread(target=start_server)
    webThread.start()
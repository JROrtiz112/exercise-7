from flask import Flask, render_template, Response
from const import systems
import json
import random

app = Flask(__name__)
system_index = -1
item_picked = {}

@app.route("/status", methods=['GET'])
def status():
    global system_index
    global item_picked

    system_index = random.randint(0,5)
    keys = list(systems.keys())
    item_picked = systems[keys[system_index]]
    
    return json.dumps({"damaged_system": keys[system_index]})

@app.route("/repair-bay", methods=['GET'])
def repairBay():
    global system_index
    global item_picked

    data = {
        'code': item_picked
    }

    return render_template('repairBay.html', data=data)

@app.route("/teapot", methods=['POST'])
def teapot():
    return Response(status=418)
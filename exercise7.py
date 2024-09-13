from flask import Flask, render_template, Response, request, abort
from const import systems
import json
import random

app = Flask(__name__)
system_index = -1
item_picked = {}

CRITICAL_PRESSURE = 10
CRITICAL_SPECIFIC_VOLUME = 0.0035
MIN_TEMPERATURE = 30

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

    if system_index == -1:
        message = "{ 'detail': 'No damaged system detected, use /status to check systems'}"
        return Response(message,status=400,mimetype='application/json')

    data = {
        'code': item_picked
    }

    return render_template('repairBay.html', data=data)

@app.route("/teapot", methods=['POST'])
def teapot():
    return Response(status=418)

@app.route("/phase-change-diagram", methods=['GET'])
def phaseChangeDiagram():
    mPa = request.args.get('pressure', type=float)
    temperature = request.args.get('temperature', type=float, default=None)
    volume = request.args.get('volume', type=float, default=None)

    if (temperature is None or temperature > MIN_TEMPERATURE) and volume is None:
        if mPa is None:
            return abort(400, description="Pressure value is expected")
        elif mPa < CRITICAL_PRESSURE:
            return abort(400, description="Pressure is lower than expected")
        elif mPa > CRITICAL_PRESSURE:
            return abort(400, description="Pressure is higher than expected")
        else:
            data = { "specific_volume_liquid": CRITICAL_SPECIFIC_VOLUME, "specific_volume_vapor": CRITICAL_SPECIFIC_VOLUME }
            return json.dumps(data)
        
    elif temperature < MIN_TEMPERATURE:
        return abort(400, description="Temperature is either below than expected or not known")
    else:
        if volume < 0.00105 and volume > 30.00:
            return abort(400, description="Volume should be between 0.00105 and 30.00 m^3/kg")
        else:
            return abort(400, description="Params such as pressure are expected")
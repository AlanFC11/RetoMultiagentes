from flask import Flask, render_template, request, jsonify
import json, logging, os, atexit
import numpy as np

from move import TrafficModel

app = Flask(__name__, static_url_path='')
m = TrafficModel(10, 36, 36, 6)
# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8585))
def positionsToJSON():
    posDICT = []
    positions = m.positions
    print(positions)
    positions = sorted(positions, key= lambda id: id[0])
    print(positions)
    for p in positions:
        pos = {
            "id": p[0],
            "x": p[1][0],
            "z": p[1][1],
            "y": 0,
            #"rotation": p[2]
        }
        posDICT.append(pos)
    return json.dumps(posDICT)


def semaforosToJSON():
    posDICT = []
    positions = m.semaforoPositions
    #positions = sorted(positions, key= lambda id: id[0])
    lights = m.getLights(36,6)
    for p in range(len(positions)):
        pos = {
            "x": positions[p][0],
            "z": positions[p][1],
            "y": 0,
            "luz": lights[p]
        }
        posDICT.append(pos)
    return json.dumps(posDICT)

@app.route('/')
def root():
    return jsonify([{"message":"Hola desde ibm"}])
@app.route('/Autos', methods=['POST','GET'])
def multiagentes():
    m.step()
    resp = "{\"data\":" + positionsToJSON()+"}"
    return resp
@app.route('/Semaforos', methods=['POST','GET'])
def multiagentes2():
    m.step()
    resp = "{\"data\":" + semaforosToJSON()+"}"
    return resp



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
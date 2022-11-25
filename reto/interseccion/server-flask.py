# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. November 2022

import numpy as np
from flask import Flask, request, jsonify
# from boids.boid import Boid
from model import IntersectionModel
import json

model = IntersectionModel()


def positionsToJSON(positions):
    posDICT = []
    for p in positions:
        pos = {
            "carId": p[0],
            "x": p[1],
            "y": p[2],
            "z": p[3]
        }
        posDICT.append(pos)
    # return jsonify({'positions': posDICT})
    return json.dumps(posDICT)


def lightStatesToJSON(lightStates):
    lightDICT = []
    for s in lightStates:
        light = {
            "lightId": s[0],
            "state": s[1]
        }
        lightDICT.append(light)
    # return jsonify({'lightStates': lightDICT})
    return json.dumps(lightDICT)


# Size of the board:
width = 16
height = 16

# Set the number of agents here:
# flock = []

app = Flask("Intersection")


@app.route('/')
def root():
    return jsonify([{
        'message': 'Hello World!'
    }])


@app.route('/init', methods=['POST', 'GET'])
def model_run():
    positions, lightStates = model.step()
    return jsonify([{
        'positions': positionsToJSON(positions),
        'lightStates': lightStatesToJSON(lightStates)
    }])


if __name__ == '__main__':
    app.run(host="localhost", port=8585, debug=True)

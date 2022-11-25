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
    count = 0
    for s in lightStates:
        light = {
            "lightId": count,
            "state": s[0]
        }
        lightDICT.append(light)
        count += 1
    # for s in range(4):
    #     light = {
    #         "state": lightStates[s]
    #     }
    #     lightDICT.append(light)
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
    [positions, lightStates] = model.step()

    ans = "{ \"positions\": " + positionsToJSON(
        positions) + ", \"lightStates\": " + lightStatesToJSON(lightStates) + " }"

    return ans


if __name__ == '__main__':
    app.run(host="localhost", port=8585, debug=True)

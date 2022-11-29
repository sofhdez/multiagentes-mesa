import mesa
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from agents import TrafficLight, Vehicle
from model import IntersectionModel


def IntersectionModel_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is TrafficLight:
        portrayal["Layer"] = 1
        portrayal["Color"] = agent.state
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["w"] = 0.5
        portrayal["h"] = 0.8
        portrayal["text"] = agent.pos
    elif type(agent) is Vehicle:
        portrayal["Layer"] = 1
        portrayal["Color"] = ["#69C7B7"]
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["r"] = 0.5
        portrayal["text"] = agent.pos
        # Change the color of the vehicle according to its speed
        if agent.speed == 1:
            portrayal["Color"] = ["#966525"]
        elif agent.speed == 2:
            portrayal["Color"] = ["#D50FDB"]
        elif agent.speed == 3:
            portrayal["Color"] = ["#812696"]
        elif agent.speed == 4:
            portrayal["Color"] = ["#048FDB"]

        if agent.emergency:
            portrayal["Color"] = ["black"]
            portrayal["r"] = 1

    return portrayal


canvas_element = CanvasGrid(IntersectionModel_portrayal, 16, 16, 600, 600)

# Charts
directions_chart = mesa.visualization.ChartModule([
    {"Label": "Vehicles_up", "Color": "Black"},
    {"Label": "Vehicles_down", "Color": "Blue"},
    {"Label": "Vehicles_left", "Color": "Brown"},
    {"Label": "Vehicles_right", "Color": "Pink"}
], data_collector_name='datacollector')

crossed_chart = mesa.visualization.ChartModule([
    {"Label": "Vehicles_crossed_up", "Color": "Black"},
    {"Label": "Vehicles_crossed_down", "Color": "Blue"},
    {"Label": "Vehicles_crossed_left", "Color": "Brown"},
    {"Label": "Vehicles_crossed_right", "Color": "Pink"}
], data_collector_name='datacollector')

model_params = {
    "nVehicles": 10}

server = ModularServer(
    IntersectionModel, [canvas_element,
                        directions_chart,
                        crossed_chart], "Traffic Simulation", model_params
)
server.port = 8521

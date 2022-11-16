import mesa
from model import IntersectionModel
from agents import StreetAgent, CarAgent, TrafficLightAgent, SidewalkAgent


def agent_portrayal(agent):
    # Portrayal method for the visualization
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}

    if type(agent) is SidewalkAgent:
        portrayal["Shape"] = "resources/grass.jpeg"
        portrayal["Layer"] = 0
        portrayal["scale"] = 1

    if type(agent) is StreetAgent:
        portrayal["Shape"] = "resources/street.jpeg"
        portrayal["Layer"] = 0
        portrayal["scale"] = 0.9

    if type(agent) is CarAgent:
        # ROTAR DEPENDIENDO DE SU DIRECCIÓN
        portrayal["Shape"] = "resources/car_top.png"
        portrayal["Layer"] = 1
        portrayal["scale"] = 1
        portrayal["id"] = agent.unique_id
        portrayal["pos"] = agent.pos
        portrayal["text_color"] = "Black"

    elif type(agent) is TrafficLightAgent:
        portrayal["Shape"] = "resources/Traffic_lights.png"
        portrayal["Layer"] = 1
        portrayal["scale"] = 0.7
        portrayal["id"] = agent.unique_id
        portrayal["pos"] = agent.pos
        portrayal["text_color"] = "Black"

        if agent.state == "green":
            portrayal["Shape"] = "resources/green.png"
            portrayal["Layer"] = 1
            portrayal["scale"] = 0.7
        elif agent.state == "yellow":
            portrayal["Shape"] = "resources/yellow.png"
            portrayal["Layer"] = 1
            portrayal["scale"] = 0.7
        elif agent.state == "red":
            portrayal["Shape"] = "resources/red.png"
            portrayal["Layer"] = 1
            portrayal["scale"] = 0.7

    return portrayal


# Create canvas and server
canvas_element = mesa.visualization.CanvasGrid(
    agent_portrayal, 16, 16, 500, 500)

server = mesa.visualization.ModularServer(
    IntersectionModel,
    [canvas_element],
    "Intersection",
    {"N": 1, "width": 16, "height": 16},
)

# Launch server
server.launch()

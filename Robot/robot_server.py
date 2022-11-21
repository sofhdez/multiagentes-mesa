import mesa

# from model import VacuumModel
from robot_agents import Box, Vacuum, Obstacle, BoxStack, VacuumModel


def agent_portrayal(agent):
    # Potrayal of agents
    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "Color": "red",
        "r": 0.4,
    }

    if type(agent) is Box:
        if agent.state == "boxe":
            portrayal["Color"] = "green"
            portrayal["Layer"] = 0
            portrayal["r"] = 0.5
            # portrayal["Shape"] = "resources/dirt.png"
            # portrayal["scale"] = 0.9
            portrayal["Layer"] = 0
            portrayal["Id"] = agent.unique_id
        else:
            portrayal["Color"] = "white"
            portrayal["Layer"] = 1
            portrayal["r"] = 0.2
            portrayal["Id"] = agent.unique_id

    elif type(agent) is Vacuum:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
        # portrayal["Shape"] = "resources/vacuum.png"
        # portrayal["scale"] = 0.9
        portrayal["robot_id"] = agent.unique_id
        portrayal["text_color"] = "black"
        portrayal["Layer"] = 1

    elif type(agent) is Obstacle:
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
        portrayal["Id"] = agent.unique_id
        portrayal["text_color"] = "black"

    elif type(agent) is BoxStack:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
        portrayal["Id"] = agent.unique_id
        portrayal["text_color"] = "black"

        if agent.state == "active":
            portrayal["Color"] = "blue"
        elif agent.state == "inactive":
            portrayal["Color"] = "yellow"
            portrayal["r"] = 0.8

    return portrayal


width = 10
height = 10

# Create canvas grid
grid = mesa.visualization.CanvasGrid(agent_portrayal, width, height, 500, 500)
# Chart of boxe cells with labels
chart = mesa.visualization.ChartModule(
    [{"Label": "boxe cells", "Color": "Black"}],
    data_collector_name="datacollector",
    # set the x axis to be the step count
    canvas_height=50,
    canvas_width=80,
)

# Pie chart of cells
pie_chart = mesa.visualization.PieChartModule(
    [
        {"Label": "boxe cells", "Color": "Brown"},
        {"Label": "Clean cells", "Color": "Blue"},
    ],
    data_collector_name="datacollector",
    # set the size of the pie chart
    canvas_height=200,
    canvas_width=200,
)

# Chart of each time each agent cleans
chart2 = mesa.visualization.ChartModule(
    [
        {"Label": "Vacuum 0", "Color": "Black"},
        {"Label": "Vacuum 1", "Color": "Blue"},
        {"Label": "Vacuum 2", "Color": "Red"},
        {"Label": "Vacuum 3", "Color": "Green"},
        {"Label": "Vacuum 4", "Color": "Yellow"},
        {"Label": "Vacuum 5", "Color": "Orange"},
    ],
    data_collector_name="datacollector",
)
# Chart show the total moves of the agents
total_moves_chart = mesa.visualization.ChartModule(
    [{"Label": "Total moves", "Color": "Black"}],
    data_collector_name="datacollector",
)

model_params = {
    # Tamaño del mundo
    "width": width,
    "height": height,
    # Número de agentes
    "N": 5,
    # Porcentaje de celdas inicialmente sucias
    # "boxeCells": mesa.visualization.Slider(
    #     "Percentage of boxe cells",
    #     0.5,
    #     0.1,
    #     1.0,
    #     0.1,
    #     description="Choose how many cells to start boxe",
    # ),
    "boxeCells": 15,
    # Tiempo máximo de ejecución.
    "max_steps": 300,
}

# Create server
server = mesa.visualization.ModularServer(
    VacuumModel,
    [grid, chart, pie_chart, chart2, total_moves_chart],
    "Robot Model Inteligente",
    model_params,
)

# Launch server
server.port = 8521  # The default
server.launch()

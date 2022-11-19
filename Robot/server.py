import mesa

from model import VacuumModel
from agents import Dirt, Vacuum


def agent_portrayal(agent):
    # Potrayal of agents
    if agent is None:
        return

    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.4}

    if type(agent) is Dirt:
        if agent.state == "Dirty":
            portrayal["Color"] = "green"
            portrayal["Layer"] = 0
            portrayal["r"] = 0.5
            # portrayal["Shape"] = "resources/dirt.png"
            # portrayal["scale"] = 0.9
            portrayal["Layer"] = 0

        else:
            portrayal["Color"] = "white"
            portrayal["Layer"] = 1
            portrayal["r"] = 0.2
    elif type(agent) is Vacuum:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
        # portrayal["Shape"] = "resources/vacuum.png"
        # portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    return portrayal


width = 10
height = 10

# Create canvas grid
grid = mesa.visualization.CanvasGrid(
    agent_portrayal, width, height, 500, 500)
# Chart of dirty cells with labels
chart = mesa.visualization.ChartModule(
    [{"Label": "Dirty cells", "Color": "Black"}],
    data_collector_name="datacollector",

    # set the x axis to be the step count
    canvas_height=50,
    canvas_width=80,
)

# Pie chart of cells
pie_chart = mesa.visualization.PieChartModule(
    [
        {"Label": "Dirty cells", "Color": "Brown"},
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
    # "N": mesa.visualization.Slider(
    #     "Number of vacuum cleaners",
    #     10,
    #     1,
    #     20,
    #     1,
    #     description="Choose how many vacuum cleaners to include in the model",
    # ),
    "N": 6,

    # Porcentaje de celdas inicialmente sucias
    # "dirtyCells": mesa.visualization.Slider(
    #     "Percentage of dirty cells",
    #     0.5,
    #     0.1,
    #     1.0,
    #     0.1,
    #     description="Choose how many cells to start dirty",
    # ),
    "dirtyCells": 0.5,

    # Tiempo máximo de ejecución.
    "max_steps": 100,
    # "max_steps": mesa.visualization.Slider(
    #     "Max steps",
    #     20,
    #     20,
    #     100,
    #     1,
    #     description="Choose the maximum number of steps to run the model",
    # ),
}

# Create server
server = mesa.visualization.ModularServer(
    VacuumModel, [grid, chart, pie_chart,
                  chart2, total_moves_chart], "Vacuum Model", model_params
)

# Launch server
server.port = 8521  # The default
server.launch()

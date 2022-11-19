import mesa
from agents import StreetAgent, CarAgent, TrafficLightAgent, SidewalkAgent


class IntersectionModel(mesa.Model):
    # Intersection model class
    def __init__(self, N, width, height):
        # Set the model's parameters
        self.N = N
        self.width = width
        self.height = height

        # Create the model's grid
        self.grid = mesa.space.MultiGrid(width, height, True)

        # Create the model's schedule
        self.schedule = mesa.time.RandomActivation(self)

        # Create the street agents
        self.create_streets()

        # Create the sidewalk agents
        self.create_sidewalks()

        # Create the model's agents
        self.create_agents()

    def create_streets(self):
        # Create the street agents
        for i in range(self.width):
            for j in range(self.height):
                # if (i > 5 and i < 6 and j > 0 and j < 5) or (i > 9 and i < 16 and j > 10 and j < 16):
                # Unique ID
                unique_id = "street" + str(i) + "_" + str(j)
                # Create a street agent
                street = StreetAgent(unique_id, self)

                # Add the street agent to the model's schedule
                self.schedule.add(street)

                # Place the street agent on the model's grid
                self.grid.place_agent(street, (i, j))

    def create_sidewalks(self):
        # Create the sidewalk agents
        for x in range(self.width):
            for y in range(self.height):
                if (x >= 0 and x <= 4):
                    if (y >= 0 and y <= 5) or (y >= 11 and y <= 15):
                        # Unique ID
                        unique_id = "sidewalk" + str(x) + "_" + str(y)

                        # Create a sidewalk agent
                        sidewalk = SidewalkAgent(unique_id, self)

                        # Add the sidewalk agent to the model's schedule
                        self.schedule.add(sidewalk)

                        # Place the sidewalk agent on the model's grid
                        self.grid.place_agent(sidewalk, (x, y))

                elif (x >= 10 and x <= 15):
                    if (y >= 0 and y <= 5) or (y >= 11 and y <= 15):
                        # Unique ID
                        unique_id = "sidewalk" + str(x) + "_" + str(y)

                        # Create a sidewalk agent
                        sidewalk = SidewalkAgent(unique_id, self)

                        # Add the sidewalk agent to the model's schedule
                        self.schedule.add(sidewalk)

                        # Place the sidewalk agent on the model's grid
                        self.grid.place_agent(sidewalk, (x, y))

    def create_agents(self):
        # Array of positions for traffic lights
        positionsXTrafficLight = [5, 9, 6, 8]
        positionsYTrafficLight = [9, 7, 6, 10]

        # Create the traffic light agents
        for i in range(4):
            # Unique ID
            unique_id = "TL" + str(i)

            # Create a traffic light agent
            traffic_light = TrafficLightAgent(unique_id, self)

            # Add the traffic light agent to the model's schedule
            self.schedule.add(traffic_light)

            # Place the traffic light agent on the model's grid
            self.grid.place_agent(
                traffic_light, (positionsXTrafficLight[i], positionsYTrafficLight[i]))

        # Array of positions for the cars
        positionsXCar = [6, 0, 15, 8]
        positionsYCar = [0, 9, 7, 15]

        # Array of directions
        directionsCar = ["up", "right", "left", "down"]

        # Create the model's agents
        for i in range(4):
            # Unique ID
            unique_id = "car" + str(i)

            # Create a car agent
            car = CarAgent(unique_id, self,
                           directionsCar[i], positionsXCar[i], positionsYCar[i])

            # Add the car agent to the model's schedule
            self.schedule.add(car)

            # Place the car agent on the model's grid
            self.grid.place_agent(car, (positionsXCar[i], positionsYCar[i]))

    def step(self):
        # Advance the model by one step
        self.schedule.step()

    def run(self, n):
        # Run the model for n steps
        for i in range(n):
            self.step()

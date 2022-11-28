import mesa
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agents import TrafficLight, Vehicle
from schedule import RandomActivationByType


class IntersectionModel(mesa.Model):
    def __init__(self, nVehicles=8, nLights=4, nSize=16):
        super().__init__()
        self.num_vehicles = nVehicles
        self.num_lights = nLights
        self.size = nSize
        self.grid = MultiGrid(nSize, nSize, False)
        self.schedule = RandomActivationByType(self)
        self.counter = 0

        self.collisions = 0

        self.datacollector = DataCollector(
            {
                "Vehicle": lambda m: m.schedule.get_type_count(Vehicle),
                "Emergency": self.count_emergency,
                "Emergency_collisions": lambda m: m.collisions,
                "TrafficLight": lambda m: m.schedule.get_type_count(TrafficLight),
                "Vehicles_up": lambda m: m.count_directions()["up"],
                "Vehicles_down": lambda m: m.count_directions()["down"],
                "Vehicles_right": lambda m: m.count_directions()["right"],
                "Vehicles_left": lambda m: m.count_directions()["left"],
                "Vehicles_crossed_left": lambda m: m.times_vehicle_crossed()["left"],
                "Vehicles_crossed_up": lambda m: m.times_vehicle_crossed()["up"],
                "Vehicles_crossed_down": lambda m: m.times_vehicle_crossed()["down"],
                "Vehicles_crossed_right": lambda m: m.times_vehicle_crossed()["right"],
            }
        )

        origin_pos = [[8, 0], [0, 7], [7, 15], [15, 8]]
        self.next_to_origin = {
            (8, 0): [0, 1, 8, 1],
            (0, 7): [1, 0, 1, 7],
            (7, 15): [0, -1, 7, 14],
            (15, 8): [-1, 0, 14, 10]
        }
        orient = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        # Create Vehicles
        for i in range(self.num_vehicles):
            rand = self.random.randint(0, 3)
            x1 = origin_pos[rand][0]
            y1 = origin_pos[rand][1]
            x2 = orient[rand][0]
            y2 = orient[rand][1]
            v = Vehicle(i, (x1, y1), (x2, y2), self)
            self.grid.place_agent(v, (x1, y1))
            self.schedule.add(v)

        pos_lig = [[6, 7], [7, 9], [8, 6], [9, 8]]
        count = 0

        # Create TrafficLights
        for i in range(self.num_vehicles, self.num_vehicles + self.num_lights):
            x = pos_lig[count][0]
            y = pos_lig[count][1]
            t = TrafficLight(i, (x, y), self)
            count += 1
            self.grid.place_agent(t, (x, y))
            self.schedule.add(t)

    def count_emergency(self):
        count = 0
        for i in range(self.num_vehicles):
            if self.schedule.agents[i].emergency:
                count += 1
        return count

    def count_directions(self):
        total_count = {
            "up": 0,
            "down": 0,
            "right": 0,
            "left": 0
        }

        for i in range(self.num_vehicles):
            direction_x = self.schedule.agents[i].direction_x
            direction_y = self.schedule.agents[i].direction_y
            direction = (direction_x, direction_y)

            if direction == (0, 1):
                key = "up"
            elif direction == (0, -1):
                key = "down"
            elif direction == (1, 0):
                key = "right"
            elif direction == (-1, 0):
                key = "left"

            if key in total_count:
                total_count[key] += 1

        return total_count

    def times_vehicle_crossed(self):
        count = {
            "left": 0,
            "up": 0,
            "down": 0,
            "right": 0,
            "other": 0
        }
        for i in range(self.num_vehicles):
            # Get current position
            pos = self.schedule.agents[i].current_pos
            # Get previous position
            prev_pos = self.schedule.agents[i].prev_pos

            # Posible positions to cross
            # pos_to_cross = [(9, 7), (8, 7), (7, 8), (7, 7)]
            pos_to_cross = [(7, 8), (8, 8), (7, 7), (8, 7)]

            # Previous position left
            prev_left = ((6, 7), (5, 7))
            # Previous position up
            prev_up = ((7, 9), (7, 10))
            # Previous position down
            prev_down = ((8, 6), (8, 5))
            # Previous position right
            prev_right = ((9, 8), (10, 8))

            if pos in pos_to_cross:
                if prev_pos in prev_left:
                    light_key = "left"
                elif prev_pos in prev_up:
                    light_key = "up"
                elif prev_pos in prev_down:
                    light_key = "down"
                elif prev_pos in prev_right:
                    light_key = "right"
                else:
                    light_key = "other"
            else:
                light_key = "other"

            if light_key in count:
                count[light_key] += 1

        # print(count)
        return count

        # Advances the model by one step
    def step(self):
        self.counter += 1
        self.datacollector.collect(self)
        self.schedule.step()

        positions = []
        for i in range(self.num_vehicles):
            car_id = self.schedule.agents[i].unique_id
            xy = self.schedule.agents[i].pos
            ambulance = self.schedule.agents[i].emergency
            p = [car_id,
                 xy[0],
                 20,
                 xy[1],
                 ambulance
                 ]
            positions.append(p)

        light_states = []
        for i in range(self.num_vehicles, self.num_vehicles + self.num_lights):
            light_id = self.schedule.agents[i].unique_id
            state = self.schedule.agents[i].state

            s = [light_id,
                 state
                 ]

            light_states.append(state)

        # Funciones para gráficos
        self.count_directions()
        self.times_vehicle_crossed()

        return positions, light_states

    def run_model(self, step=20):
        for i in range(step):
            self.step()

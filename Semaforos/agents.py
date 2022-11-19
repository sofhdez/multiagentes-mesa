import mesa


class StreetAgent(mesa.Agent):
    # Street agent class
    def __init__(self, unique_id, model):
        # Set the agent's parameters
        super().__init__(unique_id, model)

    def step(self):
        # Advance the agent by one step
        pass


class SidewalkAgent(mesa.Agent):
    # Side walk agent class
    def __init__(self, unique_id, model):
        # Set the agent's parameters
        super().__init__(unique_id, model)

    def step(self):
        # Advance the agent by one step
        pass


class CarAgent(mesa.Agent):
    # Car agent class
    def __init__(self, unique_id, model, direction, posX, posY):
        super().__init__(unique_id, model)

        # Set the agent's initial position
        self.pos = (posX, posY)

        # Set the agent's direction
        self.direction = direction

        # Set the agent's initial speed
        self.speed = 1

        # Set the agent's initial state
        self.state = "moving"

    def step(self):
        # Move the agent
        pass


class TrafficLightAgent(mesa.Agent):
    # Traffic light agent class
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        # Set the agent's initial state
        self.state = "green"

    def step(self):
        # Change the agent's state
        self.change_state()

    def change_state(self):
        # Change the agent's state if there are no cars in front of it
        if self.state == "green":
            # Check if there are cars in front of the agent
            if self.check_cars():
                self.state = "red"
        elif self.state == "red":
            if not self.check_cars():
                self.state = "green"

import mesa
import random


class TrafficLight(mesa.Agent):
    # Agent that represents a traffic light

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        # Set the position of the traffic light
        self.pos_x = pos[0]
        self.pox_y = pos[1]

        # Set the state of the traffic light
        self.state = self.set_state()

        # Set the timer of the traffic light
        self.timer = 20

    def set_state(self):
        # Set the state of the traffic light if it is in some position
        if self.pos_x == 6 or self.pos_x == 9:
            # Set to red
            return "red"
        else:
            # Set to green
            return "green"

    def change_state(self):
        # If the traffic light is red, change it to green and vice versa
        if self.state == "red":
            # Reset the timer
            self.timer = 20
            return "green"
        else:
            self.timer = 20
            return "red"

    def step(self):
        # Reduce the timer
        self.timer = self.timer - 1

        # If the timer is between 0 and 8,
        # and the state is green, change it to red
        if self.timer == 8 and self.timer > 0 and self.state == "green":
            self.state = "yellow"

        # If the timer is 0, change the state
        elif self.timer == 0:
            self.state = self.change_state()


class Vehicle(mesa.Agent):
    # Agent that represents a vehicle

    def __init__(self, unique_id, pos, direction, model):
        super().__init__(unique_id, model)
        # Set the position of the vehicle
        self.pos_x = pos[0]
        self.pos_y = pos[1]

        # Set the direction of the vehicle
        self.direction_x = direction[0]
        self.direction_y = direction[1]

        # Set the speed of the vehicle
        # self.speed = 1
        self.speed = random.randint(1, 4)

        # Set if it is an emergency vehicle
        emergency = random.randint(0, 100)
        if emergency <= 5:
            self.emergency = True
        else:
            self.emergency = False

        # Set the previous position of the vehicle
        self.prev_pos = (0, 0)

        # Set in which corner the vehicle will move
        self.corner_move = (0, 0)

        self.current_pos = (self.pos_x, self.pos_y)

    def in_edges(self, pos):
        # Check if the vehicle is in the edges
        result = (pos[0] >= 0 and pos[0] < self.model.size  # X in range
                  and pos[1] >= 0 and pos[1] < self.model.size)  # Y in range
        return result

    def in_origin(self, pos):
        # Check if the vehicle is in the origin
        result = (pos == (8, 0) or      # Down -> Up
                  pos == (0, 7) or      # Left -> Right
                  pos == (7, 15) or     # Up -> Down
                  pos == (15, 8)        # Right -> Left
                  )
        return result

    def corners(self, pos):
        # Set the direction of the vehicle in the corners of the grid

        # If the vehicle is in the down-left
        if pos[0] == 0 and pos[1] == 0:
            # Move one step up
            move = (pos[0], pos[1]+1)

            # Set the corner move to up
            self.corner_move = (0, 1)

        # If the vehicle is in the down-right
        elif pos[0] == self.model.size-1 and pos[1] == 0:
            # Move one step left
            move = (pos[0]-1, pos[1])

            # Set the corner move to left
            self.corner_move = (-1, 0)

        # If the vehicle is in the up-right
        elif pos[0] == 0 and pos[1] == self.model.size-1:
            # Move one step right
            move = (pos[0]+1, pos[1])

            # Set the corner move to right
            self.corner_move = (1, 0)

        # If the vehicle is in the up-left
        else:
            # Move one step down
            move = (pos[0], pos[1]-1)

            # Set the corner move to down
            self.corner_move = (0, -1)

        # Set the new direction of the vehicle
        self.direction_x = self.corner_move[0]
        self.direction_y = self.corner_move[1]

        # Return the new position
        return move

    def get_new_direction(self, pos):
        # Get the new direction of the vehicle
        x = pos[0]
        y = pos[1]

        # If the position is in the corners
        if (x == 0 or x == self.model.size-1) and (y == 0 or y == self.model.size-1):
            # Get the new direction
            return self.corners(pos)

        # If the position on X is in the edges and the position on Y is at the top
        if 0 <= pos[0] < self.model.size and pos[1] == self.model.size-1:
            # Move one step right
            # TODO
            x += self.speed

        # If the position on X is in the edges and the position on Y is at the bottom
        elif 0 <= pos[0] < self.model.size and pos[1] == 0:
            # Move one step left
            x -= self.speed

        # If the position on Y is in the edges and the position on X is at the right
        elif 0 <= pos[1] < self.model.size and pos[0] == self.model.size-1:
            # Move one step down
            y -= self.speed

        # If the position on Y is in the edges and the position on X is at the left
        elif 0 <= pos[1] < self.model.size and pos[0] == 0:
            # Move one step up
            y += self.speed

        # Return the new position
        new_pos = (x, y)
        return new_pos

    def step(self):
        self.move()

    def move(self):
        # Get the new position by adding the direction to the current position
        new_pos = (self.pos[0] + self.direction_x,
                   self.pos[1] + self.direction_y)

        # If the new position is not between the edges
        if self.in_edges(new_pos) == False:
            # Get the another direction
            new_pos = self.get_new_direction(self.pos)

            # If the new position is out of the edges
            if self.in_edges(new_pos) == False:
                # If the position is out of the edges on X
                if new_pos[0] < 0:
                    # Set the position on X to 0
                    new_pos = (0, new_pos[1])
                elif new_pos[0] >= self.model.size:
                    # Set the position on X to the size of the grid
                    new_pos = (self.model.size-1, new_pos[1])

                # If the position is out of the edges on Y
                if new_pos[1] < 0:
                    # Set the position on Y to 0
                    new_pos = (new_pos[0], 0)
                elif new_pos[1] >= self.model.size:
                    # Set the position on Y to the size of the grid
                    new_pos = (new_pos[0], self.model.size-1)

            # Define the previous position
            self.prev_pos = self.pos

        # Get neighbors of the new pos
        cellmates = self.model.grid.get_cell_list_contents(new_pos)

        # Check if there are any trafficlights
        trafficlights = [
            obj for obj in cellmates if isinstance(obj, TrafficLight)]

        # Check if there are any vehicles
        vehicles = [obj for obj in cellmates if isinstance(obj, Vehicle)]

        # If there are no trafficlights and no vehicles
        # and the new position is between the edges
        if len(vehicles) == 0 and len(trafficlights) == 0 and self.in_edges(new_pos) == True:
            # If the vehicle is in the origin
            if self.in_origin(self.pos):
                # Get a random direction
                rand = self.random.randint(0, 1)
                if rand == 1:
                    new_dir = self.model.next_to_origin[self.pos]
                    if self.direction_x != new_dir[0] and self.direction_y != new_dir[1]:
                        self.direction_x = new_dir[0]
                        self.direction_y = new_dir[1]

                        self.current_pos = (new_dir[2], new_dir[3])
                        self.model.grid.move_agent(
                            self, (new_dir[2], new_dir[3]))
                else:
                    self.current_pos = new_pos
                    self.model.grid.move_agent(self, new_pos)
            # If the vehicle is not in the origin
            else:
                # Set the previous position to the current position
                self.prev_pos = self.pos

                # Move the vehicle to the new position
                self.current_pos = new_pos
                self.model.grid.move_agent(self, new_pos)

        # If there are vehicles
        elif len(vehicles) != 0:
            # Don't move the vehicle
            return

        # If there are trafficlights
        elif len(trafficlights) != 0:
            # Check if the trafficlight is green
            if trafficlights[0].state == "red":
                # Don't move the vehicle
                return

            # If the trafficlight is green
            else:
                # Set the previous position to the current position
                self.prev_pos = self.pos

                # Move the vehicle to the new position
                self.current_pos = new_pos
                self.model.grid.move_agent(self, new_pos)

                # Set a new direction
                new_dir = [[0, 1, 8, 7], [1, 0, 7, 7],
                           [0, -1, 7, 8], [-1, 0, 8, 8]]
                rand = self.random.randint(0, 3)

                if self.direction_x != new_dir[rand][0] and self.direction_y != new_dir[rand][1]:
                    self.direction_x = new_dir[rand][0]
                    self.direction_y = new_dir[rand][1]

                    self.current_pos = (new_dir[rand][2], new_dir[rand][3])
                    self.model.grid.move_agent(
                        self, self.current_pos)

        else:
            self.model.grid.remove_agent(self.pos)
            self.model.schedule.remove(self)

        # If there are more than 1 agents in the same position
        if len(cellmates) >= 1:
            # Move
            self.move()
            return

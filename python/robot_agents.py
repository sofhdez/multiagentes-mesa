import mesa


class Box(mesa.Agent):
    # Agente que representa tierra
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "boxe"

    def step(self):
        pass


class Obstacle(mesa.Agent):
    # Agente que representa un obstáculo
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "obstacle"


class BoxStack(mesa.Agent):
    # Agente que representa una pila de cajas
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "active"
        self.boxes = 0
        self.cells_cleaned = 0
        self.moves = 0

    def step(self):
        if self.boxes >= 5:
            self.state = "inactive"


class Vacuum(mesa.Agent):
    # Agente que representa el aspirador
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        # Estado del agente de tipo Vacuum
        self.state = "Iniciando"

        # Se inicializa el número de movimientos
        self.moves = 0

        # Se inicializa el número de limpiezas
        self.cells_cleaned = 0

        self.nearest_stack = self.model.stacks[self.unique_id]

        self.id = unique_id

        self.visited_cells = []
        self.last_pos = ()

    def check_for_box(self):
        # Get the list of agents in the current position
        cellmates = self.model.grid.get_cell_list_contents([self.pos])

        # If there is a Dirt agent
        if any(isinstance(agent, Box) for agent in cellmates):
            # Get the Dirt agent
            box = next(agent for agent in cellmates if isinstance(agent, Box))

            # Remove the Dirt agent
            self.model.grid.remove_agent(box)

            # Increment the number of cleanings
            self.cells_cleaned += 1

            # Print the state of the Vacuum agent
            # print("Vacuum", self.unique_id, ":", self.state)

            return True

    def step(self):

        self.visited_cells.append((self.pos[0], self.pos[1]))
        if self.state == "Iniciando":
            self.state = "Moviendo"
        elif self.state == "Moviendo":
            self.move()
            if self.check_for_box():
                self.go_to_stack()
        elif self.state == "Cargando":
            self.go_to_stack()

        # Imprimir el estado del agente de tipo Vacuum
        # print(
        #     "Vacuum",
        #     self.unique_id,
        #     ":",
        #     self.state,
        #     ", stack:",
        #     self.nearest_stack.unique_id,
        #     ", pos:",
        #     self.pos,
        # )

    def move(self):
        # Obtiene la lista de las posiciones vecinas
        x_min = self.model.all_edges[0][self.unique_id][0]
        x_max = self.model.all_edges[0][self.unique_id][1]
        y_min = self.model.all_edges[1][self.unique_id][0]
        y_max = self.model.all_edges[1][self.unique_id][1]

        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False
        )

        possible_steps = list(
            set(possible_steps).difference(self.visited_cells))

        if possible_steps == []:
            # print("Random choice")
            possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=False, include_center=False
            )

        new_position = self.random.choice(possible_steps)

        # Si la posición vecina está dentro de los edges
        x_pos = new_position[0]
        y_pos = new_position[1]
        while new_position == self.last_pos or (x_pos < x_min or x_pos > x_max or y_pos < y_min or y_pos > y_max):
            new_position = self.random.choice(possible_steps)
            possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=False, include_center=False
            )
            x_pos = new_position[0]
            y_pos = new_position[1]

        # If the position is outside the edges
        # if x_pos < x_min or x_pos > x_max or y_pos < y_min or y_pos > y_max:
        #     # Get another position
        #     self.move()

        if x_pos >= x_min and x_pos <= x_max and y_pos >= y_min and y_pos <= y_max:
            # Si la posición vecina no es un obstáculo
            if not any(
                isinstance(agent, Obstacle)
                for agent in self.model.grid.get_cell_list_contents([new_position])
            ):
                # Mueve el agente de tipo Vacuum a la nueva posición
                self.model.grid.move_agent(self, new_position)
            else:
                self.visited_cells.append((x_pos, y_pos))

    def go_to_stack(self):
        # nearest_stack = self.model.stacks[0]
        if self.state == "Moviendo":

            # Change the state of the vacuum
            self.state = "Cargando"

        elif self.state == "Cargando":
            # Move to the nearest stack
            # self.model.grid.move_agent(self, nearest_stack.pos)

            if self.nearest_stack.state == "active":
                if self.pos == self.nearest_stack.pos:
                    # Change the state of the vacuum
                    self.state = "Moviendo"

                    self.nearest_stack.boxes += 1
                    # print("Vacuum", self.unique_id, ":", "Cargando")

                else:
                    self.move_to_stack(self.nearest_stack)
                    self.moves += 1
            else:
                # Set the nearest stack to the next one
                self.nearest_stack = self.model.stacks[
                    self.model.stacks.index(self.nearest_stack) + 1
                ]

    def move_to_stack(self, nearest_stack):
        # Calculate the distance to the nearest stack
        distanceX = self.pos[0] - nearest_stack.pos[0]
        distanceY = self.pos[1] - nearest_stack.pos[1]

        # First move in the X axis
        if distanceX > 0:
            new_pos = (self.pos[0] - 1, self.pos[1])
            if not any(
                isinstance(agent, Obstacle)
                for agent in self.model.grid.get_cell_list_contents([new_pos])
            ):
                self.model.grid.move_agent(self, new_pos)

            # self.model.grid.move_agent(self, (self.pos[0] - 1, self.pos[1]))
        elif distanceX < 0:
            new_pos = (self.pos[0] + 1, self.pos[1])
            if not any(
                isinstance(agent, Obstacle)
                for agent in self.model.grid.get_cell_list_contents([new_pos])
            ):
                self.model.grid.move_agent(self, new_pos)

            # self.model.grid.move_agent(self, (self.pos[0] + 1, self.pos[1]))

        # Then move in the Y axis
        if distanceY > 0:
            new_pos = (self.pos[0], self.pos[1] - 1)
            if not any(
                isinstance(agent, Obstacle)
                for agent in self.model.grid.get_cell_list_contents([new_pos])
            ):
                self.model.grid.move_agent(self, new_pos)

            # self.model.grid.move_agent(self, (self.pos[0], self.pos[1] - 1))
        elif distanceY < 0:
            new_pos = (self.pos[0], self.pos[1] + 1)
            if not any(
                isinstance(agent, Obstacle)
                for agent in self.model.grid.get_cell_list_contents([new_pos])
            ):
                self.model.grid.move_agent(self, new_pos)


def get_total_moves(model):
    total_moves = 0
    for agent in model.schedule.agents:
        if isinstance(agent, Vacuum):
            total_moves += agent.moves
    return total_moves


class VacuumModelInt(mesa.Model):
    # Modelo de la simulación
    def __init__(self, width, height, N, boxeCells, max_steps=100):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, False)
        self.schedule = mesa.time.RandomActivation(self)
        self.max_steps = max_steps
        self.running = True

        self.stacks = []

        self.all_edges = []

        self.boxeCells = boxeCells

        # Crea los obstáculos
        # Posiciones de los obstáculos
        obstacles = [
            (3, 2),
            (3, 3),
            (3, 4),
            (3, 5),
            (3, 6),
            (3, 7),
            (3, 8),
            (6, 2),
            (6, 3),
            (6, 4),
            (6, 5),
            (6, 6),
            (6, 7),
            (6, 8),
        ]
        for cell in range(len(obstacles)):
            obstacle = Obstacle(obstacles[cell], self)
            self.grid.place_agent(obstacle, obstacles[cell])

        # Crea las pilas de cajas
        # Posiciones de las pilas de cajas
        stacks_pos = [(1, 1), (1, 9), (9, 1), (9, 9), (5, 5)]
        for cell in range(len(stacks_pos)):
            stack = BoxStack(stacks_pos[cell], self)
            self.schedule.add(stack)
            self.grid.place_agent(stack, stacks_pos[cell])
            self.stacks.append(stack)

        # Crea la tierra
        for i in range(boxeCells):
            box = Box(i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            # Si la celda no está ocupada
            if not self.grid.is_cell_empty((x, y)):
                # Selecciona otra celda al azar
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)

            # print("Caja", i, ":", (x, y))

            self.grid.place_agent(box, (x, y))

        # Crea los agentes
        """
        b    x       y
        0    [0, 3]  [0, 4]
        1    [0, 3]  [5, 9]
        2    [6, 9]  [0, 4]
        3    [6, 9]  [5, 9]
        4    [4, 5]  [0, 9]
        """
        # Edges of the zone where each agent can move
        edgesX = [[0, 3], [0, 3], [6, 9], [6, 9], [4, 5]]
        edgesY = [[0, 4], [5, 9], [0, 4], [5, 9], [0, 9]]

        self.all_edges = [edgesX, edgesY]

        for i in range(self.num_agents):
            a = Vacuum(i, self)
            self.schedule.add(a)
            # Agrega el agente a una posición al azar
            x = self.random.randrange(edgesX[i][0], edgesX[i][1])
            y = self.random.randrange(edgesY[i][0], edgesY[i][1])
            # x = self.random.randrange(self.grid.width)
            # y = self.random.randrange(self.grid.height)

            # Si la posición está ocupada
            if not self.grid.is_cell_empty((x, y)):
                # Busca una posición al azar
                x = self.random.randrange(edgesX[i][0], edgesX[i][1])
                y = self.random.randrange(edgesY[i][0], edgesY[i][1])

            # Agrega el agente a la posición
            self.grid.place_agent(a, (x, y))

        # Save the model for later analysis
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "boxe cells": self.count_boxe_cells,
                "Clean cells": self.count_clean_cells,
                "Percent boxe cells": self.percent_boxe_cells,
                "Percent clean cells": self.percent_clean_cells,
                "Total moves": self.get_total_moves,
                "Vacuum 0": lambda m: m.get_agent_cleaned_cells()[0],
                "Vacuum 1": lambda m: m.get_agent_cleaned_cells()[1],
                "Vacuum 2": lambda m: m.get_agent_cleaned_cells()[2],
                "Vacuum 3": lambda m: m.get_agent_cleaned_cells()[3],
                "Vacuum 4": lambda m: m.get_agent_cleaned_cells()[4],
            },
            agent_reporters={
                "Cells cleaned": "cells_cleaned",
                "Moves": "moves",
            },
        )

    def step(self):
        # print("Stacks:", self.stacks)
        # Save the model for later analysis
        self.datacollector.collect(self)

        # Si se alcanza el número máximo de pasos
        if self.schedule.steps > self.max_steps:
            # Termina la simulación
            self.running = False

        # Si aun no se alcanza el número máximo de pasos
        elif self.schedule.steps <= self.max_steps:
            # Hasta que las pilas sumen el número de celdas boxe
            if self.get_total_boxes_in_stacks() == self.boxeCells:
                # Termina la simulación
                self.running = False
            else:
                # Ejecuta el paso de la simulación
                self.schedule.step()

        # Print counter for each stack
        # for stack in self.stacks:
            # print("Stack", stack.pos, ":", stack.boxes)

        # print("Total boxes in stacks:", self.get_total_boxes_in_stacks())

    def run_model(self):
        # Mientras la simulación se esté ejecutando
        while self.running:
            # Ejecuta el paso de la simulación
            self.step()

    def count_boxe_cells(self):
        # Cuenta el número de celdas boxe
        boxe_cells = 0
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if any(isinstance(agent, Box) for agent in cell_content):
                boxe_cells += 1
        return boxe_cells

    def percent_boxe_cells(self):
        # Calcula el porcentaje de celdas boxe
        return self.count_boxe_cells() / (self.grid.width * self.grid.height) * 100

    def count_clean_cells(self):
        # Cuenta el número de celdas Clean
        clean_cells = 0
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if not any(isinstance(agent, Box) for agent in cell_content):
                clean_cells += 1
        return clean_cells

    def percent_clean_cells(self):
        # Calcula el porcentaje de celdas Clean
        return self.count_clean_cells() / (self.grid.width * self.grid.height) * 100

    def get_total_moves(self):
        # Obtiene el número total de steps por agente
        total_moves = 0
        for agent in self.schedule.agents:
            if isinstance(agent, Vacuum):
                total_moves += agent.moves
            # total_moves += agent.moves

        return total_moves

    def get_agent_cleaned_cells(self):
        # Obtiene el número de agentes
        num_agents = len(self.schedule.agents)
        agent_cleaned_cells = []
        # Para cada agente
        for agent in self.schedule.agents:
            # Si es un agente aspiradora
            if isinstance(agent, Vacuum):
                # Obtiene el número de veces que limpia
                agent_cleaned_cells.append(agent.cells_cleaned)

        return agent_cleaned_cells

    def get_stack(self, pos):
        # Obtiene la pila de cajas en la posición pos
        cell = self.grid.get_cell_list_contents([pos])
        stack = [obj for obj in cell if isinstance(obj, BoxStack)]
        if len(stack) > 0:
            return stack[0]
        else:
            return None

    def get_total_boxes_in_stacks(self):
        # Obtiene el número total de cajas en las pilas
        total_boxes = 0
        for stack in self.stacks:
            total_boxes += stack.boxes
        return total_boxes

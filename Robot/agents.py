import mesa

# from model import VacuumModel


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

        self.nearest_stack = self.model.stacks[0]

    def check_for_box(self):
        # Get the list of agents in the current position
        cellmates = self.model.grid.get_cell_list_contents([self.pos])

        # If there is a Dirt agent
        if any(isinstance(agent, Box) for agent in cellmates):
            # Get the Dirt agent
            box = next(
                agent for agent in cellmates if isinstance(agent, Box))

            # Change the state of the Vacuum agent
            # self.state = "Aspirando"

            # Remove the Dirt agent
            self.model.grid.remove_agent(box)

            # Increment the number of cleanings
            self.cells_cleaned += 1

            # Print the state of the Vacuum agent
            # print("Vacuum", self.unique_id, ":", self.state)

            return True

    def step(self):
        if self.state == "Iniciando":
            self.state = "Moviendo"
        elif self.state == "Moviendo":
            self.move()
            if self.check_for_box():
                self.go_to_stack()
        elif self.state == "Cargando":
            self.go_to_stack()

        # Imprimir el estado del agente de tipo Vacuum
        print("Vacuum", self.unique_id, ":", self.state)

    def move(self):
        # Obtiene la lista de las posiciones vecinas
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False)

        # Selecciona una posición vecina al azar
        new_position = self.random.choice(possible_steps)

        # Si la posición vecina no es un obstáculo
        if not any(isinstance(agent, Obstacle) for agent in self.model.grid.get_cell_list_contents([new_position])):
            # Mueve el agente de tipo Vacuum a la nueva posición
            self.model.grid.move_agent(self, new_position)

        # Mueve el agente a la nueva posición
        # self.model.grid.move_agent(self, new_position)

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
                self.nearest_stack = self.model.stacks[self.model.stacks.index(
                    self.nearest_stack) + 1]

    def move_to_stack(self, nearest_stack):
        # Calculate the distance to the nearest stack
        distanceX = self.pos[0] - nearest_stack.pos[0]
        distanceY = self.pos[1] - nearest_stack.pos[1]

        # First move in the X axis
        if distanceX > 0:
            new_pos = (self.pos[0] - 1, self.pos[1])
            if not any(isinstance(agent, Obstacle) for agent in self.model.grid.get_cell_list_contents([new_pos])):
                self.model.grid.move_agent(self, new_pos)

            # self.model.grid.move_agent(self, (self.pos[0] - 1, self.pos[1]))
        elif distanceX < 0:
            new_pos = (self.pos[0] + 1, self.pos[1])
            if not any(isinstance(agent, Obstacle) for agent in self.model.grid.get_cell_list_contents([new_pos])):
                self.model.grid.move_agent(self, new_pos)

            # self.model.grid.move_agent(self, (self.pos[0] + 1, self.pos[1]))

        # Then move in the Y axis
        if distanceY > 0:
            new_pos = (self.pos[0], self.pos[1] - 1)
            if not any(isinstance(agent, Obstacle) for agent in self.model.grid.get_cell_list_contents([new_pos])):
                self.model.grid.move_agent(self, new_pos)

            #self.model.grid.move_agent(self, (self.pos[0], self.pos[1] - 1))
        elif distanceY < 0:
            new_pos = (self.pos[0], self.pos[1] + 1)
            if not any(isinstance(agent, Obstacle) for agent in self.model.grid.get_cell_list_contents([new_pos])):
                self.model.grid.move_agent(self, new_pos)


def get_total_moves(model):
    total_moves = 0
    for agent in model.schedule.agents:
        if isinstance(agent, Vacuum):
            total_moves += agent.moves
    return total_moves


class VacuumModel(mesa.Model):
    # Modelo de la simulación
    def __init__(self, width, height, N, boxeCells, max_steps=100):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, False)
        self.schedule = mesa.time.RandomActivation(self)
        self.max_steps = max_steps
        self.running = True

        self.stacks = []

        # Crea los obstáculos
        # Posiciones de los obstáculos
        obstacles = [(3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
                     (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), ]
        for cell in range(len(obstacles)):
            obstacle = Obstacle(obstacles[cell], self)
            self.grid.place_agent(obstacle, obstacles[cell])

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

            self.grid.place_agent(box, (x, y))

        # Crea las pilas de cajas
        # Posiciones de las pilas de cajas
        stacks_pos = [(1, 1), (1, 9), (9, 1), (9, 9)]
        for cell in range(len(stacks_pos)):
            stack = BoxStack(stacks_pos[cell], self)
            self.schedule.add(stack)
            self.grid.place_agent(stack, stacks_pos[cell])
            self.stacks.append(stack)

        # Crea los agentes
        for i in range(self.num_agents):
            a = Vacuum(i, self)
            self.schedule.add(a)
            # Agrega el agente a una posición al azar
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            # Si la posición está ocupada
            if not self.grid.is_cell_empty((x, y)):
                # Busca una posición al azar
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)

            # Agrega el agente a la posición
            self.grid.place_agent(a, (x, y))

            # Agrega el agente a la posición (1, 1)
            # self.grid.place_agent(a, (1, 1))

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
            # Si no hay celdas boxe
            if self.count_boxe_cells() == 0:
                # Termina la simulación
                self.running = False
            else:
                # Ejecuta el paso de la simulación
                self.schedule.step()

        # Print counter for each stack
        for stack in self.stacks:
            print("Stack", stack.pos, ":", stack.boxes)

        # Imprime el número de celdas boxe
        # print("boxe cells:", self.count_boxe_cells())

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
        # Crea una lista con el número de veces que limpia cada agente
        # agent_cleaned_cells = [0] * num_agents
        agent_cleaned_cells = []
        # Para cada agente
        for agent in self.schedule.agents:
            # Si es un agente aspiradora
            if isinstance(agent, Vacuum):
                # Obtiene el número de veces que limpia
                agent_cleaned_cells.append(agent.cells_cleaned)
                # agent_cleaned_cells[agent.unique_id] = agent.cells_cleaned
        # # Imprime el número de veces que limpia cada agente
        # print("Agent cleaned cells:", agent_cleaned_cells)

        return agent_cleaned_cells

    def get_stack(self, pos):
        # Obtiene la pila de cajas en la posición pos
        cell = self.grid.get_cell_list_contents([pos])
        stack = [obj for obj in cell if isinstance(obj, BoxStack)]
        if len(stack) > 0:
            return stack[0]
        else:
            return None

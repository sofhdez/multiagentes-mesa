import mesa

from agents import Dirt, Vacuum


class VacuumModel(mesa.Model):
    # Modelo de la simulación
    def __init__(self, width, height, N, dirtyCells, max_steps=100):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.max_steps = max_steps
        self.running = True

        # Crea los agentes
        for i in range(self.num_agents):
            a = Vacuum(i, self)
            self.schedule.add(a)
            # Agrega el agente a una posición al azar
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

            # Agrega el agente a la posición (1, 1)
            # self.grid.place_agent(a, (1, 1))

        # Crea la tierra
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if self.random.random() < dirtyCells:
                dirt = Dirt((x, y), self)
                self.grid.place_agent(dirt, (x, y))

        # Save the model for later analysis
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Dirty cells": self.count_dirty_cells,
                "Clean cells": self.count_clean_cells,
                "Percent dirty cells": self.percent_dirty_cells,
                "Percent clean cells": self.percent_clean_cells,
                "Total moves": self.get_total_moves,
                "Vacuum 0": lambda m: m.get_agent_cleaned_cells()[0],
                "Vacuum 1": lambda m: m.get_agent_cleaned_cells()[1],
                "Vacuum 2": lambda m: m.get_agent_cleaned_cells()[2],
                "Vacuum 3": lambda m: m.get_agent_cleaned_cells()[3],
                "Vacuum 4": lambda m: m.get_agent_cleaned_cells()[4],
                "Vacuum 5": lambda m: m.get_agent_cleaned_cells()[5],
            },
            agent_reporters={
                "Cells cleaned": "cells_cleaned",
                "Moves": "moves",
            },
        )

    def step(self):
        # Save the model for later analysis
        self.datacollector.collect(self)

        # Si se alcanza el número máximo de pasos
        if self.schedule.steps > self.max_steps:
            # Termina la simulación
            self.running = False

        # Si aun no se alcanza el número máximo de pasos
        elif self.schedule.steps <= self.max_steps:
            # Si no hay celdas Dirty
            if self.count_dirty_cells() == 0:
                # Termina la simulación
                self.running = False
            else:
                # Ejecuta el paso de la simulación
                self.schedule.step()

        # Imprime el número de celdas Dirty
        # print("Dirty cells:", self.count_dirty_cells())

    def run_model(self):
        # Mientras la simulación se esté ejecutando
        while self.running:
            # Ejecuta el paso de la simulación
            self.step()

    def count_dirty_cells(self):
        # Cuenta el número de celdas Dirty
        dirty_cells = 0
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if any(isinstance(agent, Dirt) for agent in cell_content):
                dirty_cells += 1
        return dirty_cells

    def percent_dirty_cells(self):
        # Calcula el porcentaje de celdas Dirty
        return self.count_dirty_cells() / (self.grid.width * self.grid.height) * 100

    def count_clean_cells(self):
        # Cuenta el número de celdas Clean
        clean_cells = 0
        for cell in self.grid.coord_iter():
            cell_content, x, y = cell
            if not any(isinstance(agent, Dirt) for agent in cell_content):
                clean_cells += 1
        return clean_cells

    def percent_clean_cells(self):
        # Calcula el porcentaje de celdas Clean
        return self.count_clean_cells() / (self.grid.width * self.grid.height) * 100

    def get_total_moves(self):
        # Obtiene el número total de steps por agente
        total_moves = 0
        for agent in self.schedule.agents:
            total_moves += agent.moves

        return total_moves

    def get_agent_cleaned_cells(self):
        # Obtiene el número de agentes
        num_agents = len(self.schedule.agents)
        # Crea una lista con el número de veces que limpia cada agente
        agent_cleaned_cells = [0] * num_agents
        # Para cada agente
        for agent in self.schedule.agents:
            # Obtiene el número de veces que limpia
            agent_cleaned_cells[agent.unique_id] = agent.cells_cleaned
        # # Imprime el número de veces que limpia cada agente
        # print("Agent cleaned cells:", agent_cleaned_cells)

        return agent_cleaned_cells

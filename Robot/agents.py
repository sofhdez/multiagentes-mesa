import mesa


class Dirt(mesa.Agent):
    # Agente que representa tierra
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "Dirty"

    def step(self):
        pass


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

    def move(self):
        # Obtiene la lista de las posiciones vecinas
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False)

        # Selecciona una posición vecina al azar
        new_position = self.random.choice(possible_steps)

        # Mueve el agente a la nueva posición
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()

        # Obtiene la lista de los agentes en la posición actual
        cellmates = self.model.grid.get_cell_list_contents([self.pos])

        # Si hay un agente de tipo Dirt
        if any(isinstance(agent, Dirt) for agent in cellmates):
            # Obtiene el agente de tipo Dirt
            dirt = next(
                agent for agent in cellmates if isinstance(agent, Dirt))

            # Cambia el estado del agente de tipo Vacuum
            self.state = "Aspirando"

            # eliminamos el agente de tipo Dirt
            self.model.grid.remove_agent(dirt)

            # Se incrementa el número de limpiezas
            self.cells_cleaned += 1

        else:
            # Cambia el estado del agente de tipo Vacuum
            self.state = "Moviendo"

            # Incrementa el número de movimientos
            self.moves += 1

        # Imprimir el estado del agente de tipo Vacuum
        # print("Vacuum", self.unique_id, ":", self.state)

# Get the times a Vacuum agent has cleaned a cell


def get_total_moves(model):
    total_moves = 0
    for agent in model.schedule.agents:
        if isinstance(agent, Vacuum):
            total_moves += agent.moves
    return total_moves

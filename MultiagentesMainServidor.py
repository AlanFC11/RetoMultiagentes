import random
import matplotlib.pyplot as plt
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import numpy as np
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid


global positionsServer
positionsServer = []

def getInitialPosition(N, RotondaSize):
    N = N-1
    calleYSize = int((N- RotondaSize)/ 2)
    listY = []
    mediumY = [int(N/2), int(N/2+1)]
    for i in range(calleYSize):
        listY.append(i)
        listY.append(N - i)
    x = random.randrange(0, N)
    while x == calleYSize+1 or x == N-calleYSize-1:
        x = random.randrange(0, N)
    if x > calleYSize and x < N-calleYSize:
        y = random.choice(listY)
    else:
        y = random.choice(mediumY)
    pos = (x, y)
    return pos


class Semaforo(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        colores = ["rojo", "verde"]
        self.luz = random.choice(colores)
        self.type = 1

    def step(self):
        colores = ["rojo", "verde"]
        self.luz = random.choice(colores)


class CarAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        #self.color = "Verde"
        self.type = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False)
        N = self.model.__getattribute__("width")
        RotondaSize = self.model.__getattribute__("RS")
        calleYSize = int((N - RotondaSize) / 2)
        rotation = 0
        #if self.type == "auto":
        # calles de enmedio
        if self.pos[0] > calleYSize and self.pos[0] < N-calleYSize-1:
            # dentro de rotonda
            if self.pos[1] == int((N / 2)-int(RotondaSize/2)):
                #new_position = (self.pos[0] + 1, self.pos[1])
                # decidir si sale en la calle o sigue girando | abajo
                if self.pos[0] < int(N / 2):
                    salida = random.randint(0, 1)
                    if salida == 0:
                        new_position = (self.pos[0] + 1, self.pos[1])
                    else:
                        new_position = (self.pos[0], self.pos[1] - 1)
                        rotation = 90
                else:
                    new_position = (self.pos[0] + 1, self.pos[1])
            elif self.pos[1] == int(N / 2) + int(RotondaSize/2):
                #decidir si sale en la calle o sigue girando | arriba
                if self.pos[0] >= int(N / 2):
                    salida = random.randint(0, 1)
                    if salida == 0:
                        new_position = (self.pos[0]-1, self.pos[1])
                    else:
                        new_position = (self.pos[0], self.pos[1]+1)
                        rotation = 90
                else:
                    new_position = (self.pos[0] - 1, self.pos[1])
            else:
                # fuera de rotonda
                #decidir direccion en base a carril izquierdo o derecho
                # arriba
                if self.pos[0] >= int(N/2):
                    new_position = (self.pos[0], self.pos[1]+1)
                    # semaforo abajo
                    if self.pos[1] == int(N / 2 - int(RotondaSize / 2) - 1) and self.pos[0] >= int(N / 2):
                        s = self.model.grid.get_cell_list_contents((N-calleYSize-1, int(N / 2 - 4)))
                        other = self.random.choice(s)
                        if other.luz == "rojo":
                            new_position = (self.pos[0], self.pos[1])
                        else:
                            new_position = (self.pos[0], self.pos[1] + 1)
                    #regresar
                    if self.pos[1]+1 >= N:
                        new_position = (self.pos[0]-1, self.pos[1])
                        rotation = -90
                # abajo
                else:
                    new_position = (self.pos[0], self.pos[1]-1)
                    # semaforo arriba
                    if self.pos[1] == int(N / 2 + int(RotondaSize / 2) + 1) and self.pos[0] < int(N / 2):
                        s = self.model.grid.get_cell_list_contents((calleYSize, int(N / 2 + 4)))
                        other = self.random.choice(s)
                        if other.luz == "rojo":
                            new_position = (self.pos[0], self.pos[1])
                        else:
                            new_position = (self.pos[0], self.pos[1] - 1)
                    #regresar
                    if self.pos[1]-1 < 0:
                        new_position = (self.pos[0]+1, self.pos[1])
                        rotation = -90

        # calles laterales
        elif self.pos[0] < calleYSize or self.pos[0] >= N-calleYSize:
            #izquierda
            if self.pos[1] == int(N/2):
                new_position = (self.pos[0] - 1, self.pos[1])
                #semaforo
                if self.pos[1] == int(N/2) and self.pos[0] == N-calleYSize:
                    s = self.model.grid.get_cell_list_contents((N-calleYSize, int(N/2+1)))
                    other = self.random.choice(s)
                    if other.luz == "rojo":
                        new_position = (self.pos[0], self.pos[1])
                    else:
                        new_position = (self.pos[0] - 1, self.pos[1])
                #regresar
                if self.pos[0] - 1 < 0:
                    new_position = (self.pos[0], self.pos[1]-1)
                    rotation = -90
            else:
                # derecha
                new_position = (self.pos[0] + 1, self.pos[1])
                #agent.luz for agent in self.model.agents
                #semaforo
                if self.pos[1] == int(N/2)-1 and self.pos[0] == calleYSize-1:
                    s = self.model.grid.get_cell_list_contents([(calleYSize-1, int(N/2-2))])
                    other = self.random.choice(s)
                    if other.luz == "rojo":
                        new_position = (self.pos[0], self.pos[1])
                    else:
                        new_position = (self.pos[0] + 1, self.pos[1])
                #regresar
                if self.pos[0] + 1 >= N:
                    new_position = (self.pos[0], self.pos[1]+1)
                    rotation = -90
        else:
            # esquinas rotonda
            if self.pos[0] == calleYSize:
                # salir de la rotonda o no lado izquierdo
                if self.pos[1] == int(N/2):
                    salida = random.randint(0, 1)
                    if salida == 0:
                        new_position = (self.pos[0] - 1, self.pos[1])
                    else:
                        new_position = (self.pos[0], self.pos[1] - 1)
                        rotation = 90

                # giros en la rotonda
                elif self.pos[1] == int(N / 2-int(RotondaSize/2)):
                    new_position = (self.pos[0] + 1, self.pos[1])
                    rotation = -90
                else:
                    new_position = (self.pos[0], self.pos[1] - 1)
                    rotation = 90
            elif self.pos[0] == N-calleYSize-1:
                # salir de la rotonda o no lado derecho
                if self.pos[1] == int(N / 2) - 1:
                    salida = random.randint(0, 1)
                    if salida == 0:
                        new_position = (self.pos[0] + 1, self.pos[1])
                    else:
                        new_position = (self.pos[0], self.pos[1] + 1)
                        rotation = 90
                # giros en la rotonda
                elif self.pos[1] == int(N / 2+int(RotondaSize/2)):
                    new_position = (self.pos[0] - 1, self.pos[1])
                    rotation = -90
                else:
                    new_position = (self.pos[0], self.pos[1] + 1)
                    rotation = 90

        #new_position = (self.pos[0]+1, self.pos[1])
        if self.model.grid.is_cell_empty(new_position):
            self.model.grid.move_agent(self, new_position)
        #global positionsServer
        self.model.appendPos([self.unique_id, new_position, rotation])
    #else:
        #new_position = (calleYSize, int(N/2))
        #self.model.grid.move_agent(self, new_position)

    def step(self):
        try:
            self.move()
            #self.model.__setattr__("positions", [])
            #self.model.
        except:
            print("error")
        #global positionsServer
        #positions = positionsServer
        #print(positionsServer)
        #if self.color == "Verde":
            #print("semaforo en verde")


class TrafficModel(Model):
    def __init__(self, N, width, height, RS):
        self.num_agents = N
        #self.num_semaforos = 1
        self.width = width
        self.RS = RS
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.positions = []
        calleSize = int((width - RS) / 2)
        self.semaforoPositions = [(calleSize-1, int(width/2-2)), (calleSize, int(width/2+4)), (width-calleSize-1, int(width/2-4)),
                      (width-calleSize, int(width/2+1))]
        # Create agents

        for i in range(self.num_agents):
            a = CarAgent(i, self)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            pos = getInitialPosition(width, RS)
            while not self.grid.is_cell_empty(pos):
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                pos = getInitialPosition(width,RS)
            self.grid.place_agent(a, pos)
            #global positionsServer
            self.positions.append([i, pos, 0])
            #self.grid.position_agent(a)

        calleSize = int((width - RS) / 2)
        self.semaforoPositions = [(calleSize-1, int(width/2-2)), (calleSize, int(width/2+4)), (width-calleSize-1, int(width/2-4)),
                      (width-calleSize, int(width/2+1))]
        for i in range(4):
            s = Semaforo(i+self.num_agents, self)
            self.schedule.add(s)
            self.grid.place_agent(s, self.semaforoPositions[i])

    def getLights(self, width, RS):
        calleSize = int((width - RS) / 2)
        luces = []
        semaforoPos = [(calleSize - 1, int(width / 2 - 2)), (calleSize, int(width / 2 + 4)),
                       (width - calleSize - 1, int(width / 2 - 4)),
                       (width - calleSize, int(width / 2 + 1))]
        for i in range(len(semaforoPos)):
            s = self.grid.get_cell_list_contents(semaforoPos[i])
            other = self.random.choice(s)
            luces.append(other.luz)
        return luces

    def appendPos(self, pos):
        self.positions.append(pos)

    def updateMove(self):
        self.positions = []

    def step(self):
        self.updateMove()
        self.schedule.step()


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}
    if agent.type == 0:
        #portrayal["w"] = 31
        #portrayal["h"] = 5
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
    elif agent.type == 1:
        if agent.luz == "rojo":
            portrayal["Color"] = "red"
        else:
            portrayal["Color"] = "green"
        portrayal["Layer"] = 0

    return portrayal


if __name__ == '__main__':

    grid = CanvasGrid(agent_portrayal, 28, 28, 600, 600)
    server = ModularServer(TrafficModel,
                           [grid],
                           "Traffic Model",
                           {"N": 10, "width": 28, "height": 28, "RS": 6})
    server.port = 8521  # The default
    server.launch()







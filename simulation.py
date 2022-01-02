import tkinter as tk
from queue import PriorityQueue
from functools import partial
from collections import defaultdict
import tkinter.font as tkFont

class App:

    # Colors:
    purple = "#b48ead"
    red = "#bf616a"
    grey = "#2e3440"
    green = "#a3be8c"
    blue = "#5e81ac"
    white = "#eceff4"

    # States
    noState = "None"
    startState = "Start State"
    goalState = "Goal State"
    road = " Road"

    # Data Structures
    selectedOption = noState
    startingState = ()
    goalStates = ()
    roadStates = {}

    def __init__(self, root):
        #setting title
        root.title("Path Finding Simulator")
        #setting window size
        width=1000
        height=805
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # Radio Button:
        heuristic=tk.Radiobutton(root)
        heuristic["fg"] = self.white
        heuristic["justify"] = "center"
        heuristic["text"] = "Manhattan Distance"
        heuristic.place(x=810,y=100,width=200,height=20)
        # GRadio_660["command"] = self.GRadio_660_command

        #Start Button 
        startButton=tk.Button(root)
        startButton["activebackground"] = "#4c566a"
        startButton["activeforeground"] = "#d8dee9"
        startButton["bg"] = "#d8dee9"
        startButton["borderwidth"] = "0px"
        startButton["fg"] = "#2e3440"
        startButton["text"] = "Start Simulation"
        startButton.place(x=810,y=720,width=180,height=40)
        startButton["command"] = self.solve

        # Reset
        Reset=tk.Button(root)
        Reset["bg"] = "#2e3440"
        Reset["activeforeground"] = "#d8dee9"
        Reset["borderwidth"] = "0px"
        Reset["fg"] = "#eceff4"
        Reset["text"] = "Reset"
        Reset.place(x=810,y=400,width=180,height=40)
        Reset["command"] = self.Reset

        # Message
        self.Message=tk.Message(root)
        self.Message["fg"] = self.grey
        self.Message["bg"] = self.white
        self.Message["justify"] = "center"
        ft = tkFont.Font(family='Times',size=16)
        self.Message["font"] = ft
        self.Message.place(x=810,y=150,width=200,height=200)

        # Start State Set Button
        startState=tk.Button(root)
        startState["bg"] = "#2e3440"
        startState["activeforeground"] = "#d8dee9"
        startState["borderwidth"] = "0px"
        startState["fg"] = "#eceff4"
        startState["text"] = "Set Start State"
        startState.place(x=810,y=480,width=180,height=40)
        startState["command"] = self.setStartState

        # Goal State Set Button
        goalState=tk.Button(root)
        goalState["bg"] = "#2e3440"
        goalState["activeforeground"] = "#d8dee9"
        goalState["borderwidth"] = "0px"
        goalState["fg"] = "#eceff4"
        goalState["text"] = "Set Goal State"
        goalState.place(x=810,y=560,width=180,height=40)
        goalState["command"] = self.setGoalState

        # Set Obstacles Button
        obstacleState=tk.Button(root)
        obstacleState["bg"] = "#2e3440"
        obstacleState["activeforeground"] = "#d8dee9"
        obstacleState["borderwidth"] = "0px"
        obstacleState["fg"] = "#eceff4"
        obstacleState["text"] = "Set Road"
        obstacleState.place(x=810,y=640,width=180,height=40)
        obstacleState["command"] = self.setRoad

        # Populate Grid
        self.cells = {}
        for row in range(40):
            for col in range(40):
                btn=tk.Button()
                
                btn["bg"] = "#a3be8c"
                btn["borderwidth"] = "0px"
                btn["fg"] = "#2e3436"
                btn["text"] = ""
                btn.place(x=row*20,y=col*20,width=20,height=20)
                btn["command"] = partial(self.btn_click,(row, col))

                self.cells[(row,col)] = btn
        
        # Verticle Divider Label
        divider=tk.Label(root)
        divider["bg"] = "#4c566a"
        divider["text"] = ""
        divider.place(x=800,y=0,width=3,height=800)

        # Horizontal Divider:
        divider2=tk.Label(root)
        divider2["bg"] = "#4c566a"
        divider2["text"] = ""
        divider2.place(x=800,y=390,width=200,height=3)



    # Option Label
        self.option=tk.Label(root)
        self.option["fg"] = "#d8dee9"
        self.option["text"] = "Selection: " + self.selectedOption
        self.option.place(x=810,y=40,width=180,height=40)

    
    # Click Actions
    def btn_click(self, rc):
        if self.selectedOption is self.startState and rc not in self.goalStates and rc not in self.roadStates:

            # key = self.startingState.keys()
            # for k in key:
            if self.startingState:
                self.cells[self.startingState]["bg"] = self.green
            
            self.startingState = rc
            self.cells[rc]["bg"] = self.purple
            # self.startingState[rc] = self.cells[rc]

        elif self.selectedOption is self.goalState and rc not in self.startingState and rc not in self.roadStates:
            
            # key = self.goalStates.keys()
            # for k in key:
            if self.goalStates:
                self.cells[self.goalStates]["bg"] = self.green
                
            self.goalStates = rc
            self.cells[rc]["bg"] = self.red
            # self.goalStates[rc] = self.cells[rc]

        elif self.selectedOption is self.road and rc not in self.startingState and rc not in self.goalStates:
            self.cells[rc]["bg"] = self.grey

            row_right = (rc[0]+1, rc[1])
            row_left = (rc[0]-1, rc[1])

            col_top = (rc[0], rc[1] - 1)
            col_bottom = (rc[0], rc[1] + 1)

            if col_top in self.roadStates.keys() or col_bottom in self.roadStates.keys():
                self.cells[rc]["text"] = "|"
            if row_right in self.roadStates.keys() or row_left in self.roadStates.keys():
                self.cells[rc]["text"] = "--"
 
            self.cells[rc]["fg"] = "#d8dee9"
            self.roadStates[rc] = self.cells[rc]


    def Reset(self):

        for node in self.cells.keys():
           self.cells[node]["bg"] = "#a3be8c"
           self.cells[node]["borderwidth"] = "0px"
           self.cells[node]["text"] = ""
        
        self.roadStates.clear()
        self.startingState = ()
        self.goalStates = ()
        self.Message["text"] = ""
        

    def setStartState(self):
       self.selectedOption = self.startState
       self.option["text"] = "Selection: " + self.selectedOption


    def setGoalState(self):
       self.selectedOption = self.goalState
       self.option["text"] = "Selection: " + self.selectedOption


    def setRoad(self):
        self.selectedOption = self.road
        self.option["text"] = "Selection: " + self.selectedOption
    
    
    def h(self, x):
        return abs(x[0] - self.goalStates[0]) + abs(x[1] - self.goalStates[1])

    def neighborOf(self, current):

        neighbors = []
        neighbors.append((current[0] + 1, current[1]))
        neighbors.append((current[0] - 1, current[1]))
        neighbors.append((current[0], current[1] + 1))
        neighbors.append((current[0], current[1] - 1))

        return neighbors
    
    def reconstruct_path(self,cameFrom):
        current = self.goalStates
        final_path = []

        while current != self.startingState:
            current = cameFrom[current]
            final_path.append(current)
        final_path.pop()
        return final_path


    def solve(self):

        if not self.startingState or not self.goalStates:
            self.Message["text"] = "Set Start and Goal States First"
        else:

            x = self.startingState
            isfound = False
            openSet = PriorityQueue()
            
            cameFrom = {}
            
            g = defaultdict(lambda: float('inf'))
            g[x] = 0

            f = defaultdict(lambda: float('inf'))
            f[x] = self.h(x)

            openSet.put((f[x], x))

            while not openSet.empty():
                current = openSet.get()
                
                if current[1] == self.goalStates:
                    self.Message["text"] = "Optimal Path Found!"
                    isfound = True
                    nodes = self.reconstruct_path(cameFrom)
                    for node in nodes:
                        self.cells[node]["bg"] = self.blue
                    break
                else:
                    self.cells[current[1]]["bg"] = "#ebcb8b"
                    for neighbor in self.neighborOf(current[1]):
                        g_current = g[current[1]] + 1
                        
                        if g_current < g[neighbor]:
                            cameFrom[neighbor] = current[1]
                            g[neighbor] = g_current
                            f[neighbor] = g[neighbor] + self.h(neighbor)

                            if neighbor not in openSet.queue and (neighbor in self.roadStates.keys() or neighbor == self.goalStates):
                                openSet.put((f[neighbor],neighbor))
            if not isfound:
                self.Message["text"] = "No Optimal Path Found!"


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
 

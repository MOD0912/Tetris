'''
Mielvin Kapferer
'''

import time
import random
import customtkinter as ctk
from english_words import get_english_words_set



ctk.deactivate_automatic_dpi_awareness()

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tetris")
        self.attributes("-fullscreen", True)
        rows = (1)
        cols = (1)
        self.main_frame = ctk.CTkFrame(self)   
        self.rowconfigure(rows, weight=5)
        self.columnconfigure(cols, weight=5)
        rows = (0, 2)
        cols = (0, 2)
        self.rowconfigure(rows, weight=1)
        self.columnconfigure(cols, weight=1)
        self.main_frame.grid(row=1, column=1)
        rows = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19)
        cols = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        self.main_frame.rowconfigure(rows, weight=1)
        self.main_frame.columnconfigure(cols, weight=1)
        
        self.row = 0
        self.col = 0
        self.labels = []
        self.coordinates= []
        self.after(100, self.placeholder)
        


    
    
    def placeholder(self):
        for i in range(20):
            ctk.CTkLabel(self.main_frame, text=" ", height=50, width=50).grid(row=i, column=0, sticky="nsew")
        for i in range(10):
            ctk.CTkLabel(self.main_frame, text=" ", width=50, height=50).grid(row=0, column=i, sticky="nsew")




class Logic:
    def __init__(self):
        self.cl = True
        self.active_labels = []                                                                                   
        actions = ["<Left>", "<Right>", "<Down>", "<space>"]
        self.end = False
        for action in actions:
            gui.bind(action, self.move)
        
        #gui.bind("<Up>", self.spawn_random)
        gui.bind("<space>", self.move)
        
        #self.figures = [[(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 0), (0, 1), (0, 2), (1, 0)], [(0, 0), (0, 1), (0, 2), (1, 2)], [(0, 0), (0, 1), (0, 2), (1, 1)], [(0, 0), (0, 1), (0, 2), (1, 2)], [(0, 0), (0, 1), (0, 2), (1, 0)], [(0, 0), (0, 1), (0, 2), (1, 1)]]
        #move every figure to the right
        self.figures = [                                  # Shapes:
                        [0, (4, 0), (4, 1), (4, 2), (4, 3)], # line
                        [1, (4, 0), (4, 1), (4, 2), (5, 2)], # L
                        [2, (4, 0), (4, 1), (4, 2), (5, 1)], # T right
                        [3, (4, 0), (4, 1), (4, 2), (5, 0)], # reverse L
                        [4, (4, 0), (4, 1), (5, 0), (5, 1)], # square
                        [5, (4, 0), (4, 1), (5, 1), (5, 2)], # Z
                        [6, (4, 0), (4, 1), (5, 0), (5, 1)]  # reverse Z
                        ]
        self.pos_labels = [[" " for i in range(10)] for j in range(20)]
        self.cl_time = 500
        self.check()
        gui.after(200, self.spawn_random)


    def rotate_figure(self):
        min_row = min(i.row for i in self.active_labels)
        min_col = min(i.col for i in self.active_labels)
        max_row = max(i.row for i in self.active_labels)
        max_col = max(i.col for i in self.active_labels)
        center_row = (min_row + max_row) // 2
        center_col = (min_col + max_col) // 2
        new_positions = []
        for i in self.active_labels:
            new_row = center_col - (i.col - center_col)
            new_col = center_row + (i.row - center_row)
            # Check if the new position is within the grid and doesn't collide with existing figures
            if new_row < 0 or new_row > 19 or new_col < 0 or new_col > 9 or self.pos_labels[new_row][new_col] != " ":
                return
            new_positions.append((new_row, new_col))
        # Update the positions of the labels and the pos_labels list
        for i in zip(self.active_labels, new_positions):
            i[0].row, i[0].col = i[1]
            self.pos_labels[i[0].row][i[0].col] = i[0]
            self.pos_labels[i[1][0]][i[1][1]] = " "
        # Update the grid positions of the labels
        for i in self.active_labels:
            i.grid(row=i.row, column=i.col, sticky="nsew")

    def clock(self):
        retur = False
        for i in self.active_labels:
            i.row += 1
            i.grid(row=i.row, column=i.col, sticky="nsew")
            if i.row == 19 or self.pos_labels[i.row+1][i.col] != " ":
                print("retur")
                retur = True
            else:
                print(i.row, i.col)
                i.moved = True
        
        if retur:
            self.moved = False
            for i in self.active_labels:
                self.pos_labels[i.row][i.col] = i
                if i.moved:
                    self.moved = True
            
            if not self.moved:
                print("game over")
                self.end = True
            self.active_labels.clear()
        
            self.spawn_random()
            print("clear")
            return
        gui.after(self.cl_time, self.clock)
        
    def check(self):
        for i in self.pos_labels:
            if " " not in i:
                print("full")
                index = self.pos_labels.index(i)
                self.pos_labels.remove(i)
                self.pos_labels.insert(0, [" " for i in range(10)])
                print(gui.labels)
                x = gui.labels.copy()
                for j in x:
                    print(j)
                    if j.row == index:
                        j.destroy()
                        gui.labels.remove(j)
                print()
                print(index)
                print()
                for j in gui.labels:
                    if j.row < index:
                        print(j.row)
                        j.row += 1
                        j.grid(row=j.row, column=j.col, sticky="nsew")
                    
        gui.after(100, self.check)

    def spawn_random(self, event=None):
        if self.end:
            return
        random_figure = random.choice(self.figures)
        color = random.choice(["red", "blue", "green", "yellow", "purple", "orange", "pink"])
        for i in random_figure:
            if type(i) == int:
                continue
            self.active_labels.append(Create_Label(gui.main_frame, color, i[0], i[1]))
        self.cl_time = 500
        self.clock()


    def move(self, event):
        var = event.keysym
        if var == "Left":
            for i in self.active_labels:
                if i.col == 0 or self.pos_labels[i.row][i.col-1] != " ":
                    return
            for i in self.active_labels:
                i.col -= 1
                i.grid(row=i.row, column=i.col, sticky="nsew")  

            for i in self.pos_labels:
                lst = []
                for j in i:
                    lst.append((j.row, j.col) if j != " " else " ")
                print(lst)

        if var == "Right":
            for i in self.active_labels:
                if i.col == 9 or self.pos_labels[i.row][i.col+1] != " ":
                    return
                
            for i in self.active_labels:
                i.col += 1
                i.grid(row=i.row, column=i.col, sticky="nsew")  
        
        if var == "space":
            self.rotate_figure()
                
        
        if var == "Down":
            self.cl_time = 100
    
        print(event.keysym)
            
        
class Create_Label(ctk.CTkLabel):
    def __init__(self, main_frame, color, col, row):
        super().__init__(main_frame, fg_color=color, text="", height=50, width=50)
        self.col = col
        self.row = row
        self.moved = False

        self.grid(row=self.row, column=self.col, sticky="nsew") 
        gui.labels.append(self)
    


if __name__ == "__main__":
    gui = GUI()
    logic = Logic()
    gui.mainloop()
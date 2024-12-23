import customtkinter as ctk
ctk.deactivate_automatic_dpi_awareness()
import time
import random
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
        for action in actions:
            gui.bind(action, self.move)
        
        gui.bind("<Up>", self.spawn_random)
        gui.bind("<space>", self.move)
        
        self.figures = [[(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 0), (0, 1), (0, 2), (1, 0)], [(0, 0), (0, 1), (0, 2), (1, 2)], [(0, 0), (0, 1), (0, 2), (1, 1)], [(0, 0), (0, 1), (0, 2), (1, 2)], [(0, 0), (0, 1), (0, 2), (1, 0)], [(0, 0), (0, 1), (0, 2), (1, 1)]]
        # self.figures = [[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]]
        # self.figures = [[(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1)]]
        self.pos_labels = [[" " for i in range(10)] for j in range(20)]
        self.cl_time = 500
        self.check()
        gui.after(200, self.spawn_random)


   
    def clock(self):
        retur = False
        for i in self.active_labels:
            i.row += 1
            i.grid(row=i.row, column=i.col, sticky="nsew")
            if i.row == 19 or self.pos_labels[i.row+1][i.col] != " ":
                retur = True
        
        if retur:
            for i in self.active_labels:
                self.pos_labels[i.row][i.col] = i
            self.active_labels.clear()
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
        random_figure = random.choice(self.figures)
        for i in random_figure:
            self.active_labels.append(Create_Label(gui.main_frame, i[0], i[1]))
        self.clock()


    def move(self, event):
        var = event.keysym
        if var == "Left":
            for i in self.active_labels:
                if i.col == 0:
                    return
            for i in self.active_labels:
                i.col -= 1

        if var == "Right":
            for i in self.active_labels:
                if i.col == 9:
                    return
            for i in self.active_labels:
                i.col += 1
        
        if var == "space":
            for i in self.pos_labels:
                print(i)
        
        if var == "Down":
            self.cl_time = 100
    
        print(event.keysym)
            
        
        
class Create_Label(ctk.CTkLabel):
    def __init__(self, main_frame, col, row):
        super().__init__(main_frame, fg_color="red", text="", height=50, width=50)
        self.col = col
        self.row = row
        self.grid(row=self.row, column=self.col, sticky="nsew") 
        gui.labels.append(self)
    


        

if __name__ == "__main__":
    gui = GUI()
    logic = Logic()
    gui.mainloop()
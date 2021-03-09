import tkinter as tk

lastx, lasty = None, None
lastIndex = None

class App(tk.Tk):
    radius = 15
    graph = []
    id_grap = []
    graph_matrix = []
    color_list = ["green", "blue", "orange", "black", "#693c72", "#c15050", "#d97642", "#d49d42", "#f0e4d7", "#440a67", "#93329e", "#b4aee8", "#ffe3fe"]

    def __init__(self):
        super().__init__()
        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.select_circle)
        self.canvas.bind('<Shift-1>', self.make_circle)
        self.canvas.bind('<Control-1>', self.color)

        self.selected = None

    def make_circle(self, event):
        x, y, r = event.x, event.y, self.radius
        self.graph.append([x, y])
        id = self.canvas.create_oval(x-r, y-r, x+r, y+r, outline='black', fill='white')
        self.id_grap.append(id)
        length = len(self.graph_matrix)
        if length == 0:
            self.graph_matrix = [[0]]
        else:
            self.graph_matrix.append([0 for x in range(length)])
            self.graph_matrix = [x + [0] for x in self.graph_matrix]

    def select_circle(self, event):
        global lastx, lasty, lastIndex
        # self.canvas.bind('<Motion>', self.move_circle)
        self.canvas.bind('<ButtonRelease-1>', self.deselect)
        self.canvas.addtag_withtag('selected', tk.CURRENT)
        position = self.canvas.coords('selected')
        if position == []: return
        x = position[0] + self.radius
        y = position[1] + self.radius
        index = self.graph.index([int(x), int(y)])
        if lastx == None and lasty == None and lastIndex == None:
            lastx = x
            lasty = y
            lastIndex = index
        else:
            if self.graph_matrix[index][lastIndex] == 1:
                lastIndex, lastx, lasty = None, None, None
                return
            self.canvas.create_line((lastx, lasty, x, y), width=1)
            self.graph_matrix[index][lastIndex] = 1
            self.graph_matrix[lastIndex][index] = 1
            lastIndex, lastx, lasty = None, None, None

    # def move_circle(self, event): comming soon...
    #     x, y, r = event.x, event.y, self.radius
    #     self.canvas.coords('selected', x-r, y-r, x+r, y+r)

    def deselect(self, event):
        self.canvas.dtag('selected')
        self.canvas.unbind('<Motion>')
        self.canvas.bind('<Shift-1>', self.make_circle)
    
    def color(self, event):
        # result = [0 for ele in self.graph_matrix]
        matrix = [[ix, ele[0], sum(ele[1]), 0] for ix, ele in zip(self.id_grap, enumerate(self.graph_matrix))]
        matrix = sorted(matrix, key=lambda k: k[2], reverse=True)
        num_color = 0
        for i in self.graph_matrix:
            print(i)
        for ix in range(len(matrix)):
            if matrix[ix][3] == 0:
                matrix[ix][3] = num_color + 1
                self.canvas.itemconfigure(matrix[ix][0], fill=self.color_list[matrix[ix][3]])
                # print(result)
                for i in range(ix + 1, len(matrix)):
                    if matrix[i][3] == 0 and \
                        self.graph_matrix[matrix[ix][1]][matrix[i][1]] == 0 and \
                        self.isColor(matrix[i][1], num_color + 1, matrix) == True:
                        matrix[i][3] = num_color + 1
                        self.canvas.itemconfigure(matrix[i][0], fill=self.color_list[matrix[i][3]])
            num_color += 1
    
    def isColor(self, row, color, matrix):
        print(self.graph_matrix[row])
        for ix, point in enumerate(self.graph_matrix[row]):
            if point == 1:
                print(row, ix)
                for x in matrix:
                    if x[1] == ix and x[3] == color:
                        return False
        
        return True




if __name__ == '__main__':

    App().mainloop()
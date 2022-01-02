from tkinter.constants import TRUE
from game_of_life import Game
import time
import tkinter as tk

class LifeGameCanvas(tk.Canvas):
    def __init__(self, cell_size, *args, **kwargs):
        super().__init__(bg="white", *args, **kwargs)
        self.cell_size = cell_size
        self.bind("<Button-1>", self.event_edit_maker(self.create_cell))
        self.bind("<Button-3>", self.event_edit_maker(self.remove_cell))
        self.cells = []
        self.edit = True

    def get_cells(self):
        return tuple(self.cells)

    def render_cells(self, cells):
        self.edit = False
        self.delete("all")
        self.cells = list(cells)
        for x, y in cells:
            self.create_cell(x, y)

    def event_edit_maker(self, func):
        def event_func(event):
            if self.edit:
                x, y = event.x, event.y
                x //= self.cell_size[0]
                y //= self.cell_size[1]
                func(x, y)
        return event_func

    def create_cell(self, x, y):
        (x0, y0), (x1, y1) = self.convert_coordinates(x, y)
        self.create_rectangle(x0, y0, x1, y1, fill="black", outline="")
        self.cells.append((x, y))

    def remove_cell(self, x, y):
        (x0, y0), (x1, y1) = self.convert_coordinates(x, y)
        self.create_rectangle(x0, y0, x1, y1, fill="white", outline="")
        if (x, y) in self.cells:
            self.cells.remove((x, y))

    def convert_coordinates(self, x, y):
        dx, dy = self.cell_size
        return (x*dx, y*dy), ((x+1)*dx, (y+1)*dy)


class Cycle:
    def __init__(self, canvas, delay):
        self.canvas = canvas
        self.delay = delay
        self.game = None

    def __call__(self):
        self.game = Game(self.canvas.get_cells())
        self.update()

    def update(self):
        self.game.update()
        self.canvas.render_cells(self.game.get_cells())
        self.canvas.after(self.delay, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Game of Life")
    
    canvas = LifeGameCanvas(master=root, width=500, height=500, cell_size=(10, 10))
    canvas.pack()

    btn = tk.Button(master=root, text="Start Game!", command=Cycle(canvas, 1000))
    btn.pack(side="bottom")
    
    root.mainloop()
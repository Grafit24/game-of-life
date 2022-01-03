from game_of_life import Game
import tkinter as tk

class LifeGameCanvas(tk.Canvas):
    def __init__(self, cell_size, height, width, *args, **kwargs):
        super().__init__(bg="white", height=height, width=width, *args, **kwargs)
        self.cell_size = cell_size
        self.bind("<Button-1>", self.event_edit_maker(self.create_cell))
        self.bind("<Button-3>", self.event_edit_maker(self.remove_cell))
        self.bind("<B2-Motion>", self.move_camera)
        self.configure(xscrollincrement=1, yscrollincrement=1)
        self.width = width
        self.height = height
        self.center = (int(width/2), int(height/2))
        self.cells = []
        self.camera_coef = 3
        self.camera_pos = (0, 0)
        self.edit = True

    def get_cells(self):
        return tuple(self.cells)

    def render_cells(self, cells):
        self.edit = False
        self.delete("all")
        self.cells = list(cells)
        for x, y in cells:
            self.create_cell(x, y)

    def move_camera(self, event):
        vector = (-(self.center[0]-event.x), -(self.center[1]-event.y))
        x_dir, y_dir = vector
        x_dir = self.camera_coef*x_dir//self.center[0]
        y_dir = self.camera_coef*y_dir//self.center[1]
        self.camera_pos = self.camera_pos[0]+x_dir, self.camera_pos[1]+y_dir
        print(self.camera_pos)
        self.xview_scroll(x_dir, "units")
        self.yview_scroll(y_dir, "units")

    def event_edit_maker(self, func):
        def event_func(event):
            if self.edit:
                x, y = event.x, event.y
                x, y = self.camera_pos[0]+x, self.camera_pos[1]+y
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
    def __init__(self, canvas, delay=100):
        self.canvas = canvas
        self.delay = delay
        self.game = Game()
        self.stop = False

    def start(self):
        self.stop = False
        self.game.init(self.canvas.get_cells())
        self.update()

    def update(self):
        if not self.stop:
            self.game.update()
            self.canvas.render_cells(self.game.get_cells())
            self.canvas.after(self.delay, self.update)

    # TODO Test quit
    def quit(self):
        self.canvas.edit = True
        self.canvas.delete("all")
        self.canvas.cells = []
        self.stop = True
        

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Game of Life")
    
    canvas = LifeGameCanvas(master=root, width=500, height=500, cell_size=(10, 10))
    canvas.pack()

    cycle = Cycle(canvas)
    start_button = tk.Button(master=root, text="Start Cycle", command=cycle.start)
    start_button.pack(side="left")
    refresh_button = tk.Button(master=root, text="Stop Cycle", command=cycle.quit)
    refresh_button.pack(side="left")
    # TODO Delay editing
    delay_entry = tk.Entry()
    delay_entry.pack(side="left")
    
    root.mainloop()
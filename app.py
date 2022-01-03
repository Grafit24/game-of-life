from game_of_life import Game
import tkinter as tk

class LifeGameCanvas(tk.Canvas):
    def __init__(self, cell_size, height, width, *args, **kwargs):
        super().__init__(bg="white", height=height, width=width, *args, **kwargs)
        # Additional
        self.width = width
        self.height = height
        self.xcenter, self.ycenter = int(width/2), int(height/2)
        # Rendering
        self.cell_size = cell_size
        self.cells = []
        # Camera
        # set unit measurement 
        self.configure(xscrollincrement=1, yscrollincrement=1)
        self.bind("<B2-Motion>", self.move_camera)
        self.camera_coef = 3
        self.xcamera, self.ycamera = 0, 0
        # Edit
        self.edit = True
        self.bind("<Button-1>", self.event_edit_maker(self.create_cell))
        self.bind("<Button-3>", self.event_edit_maker(self.remove_cell))

    def get_cells(self):
        return tuple(self.cells)

    def render_cells(self, cells):
        self.edit = False
        self.delete("all")
        self.cells = list(cells)
        for x, y in cells:
            self.create_cell(x, y)

    def move_camera(self, event):
        vector = (-(self.xcenter-event.x), -(self.ycenter-event.y))
        x_dir, y_dir = vector
        x_dir = self.camera_coef*x_dir//self.xcenter
        y_dir = self.camera_coef*y_dir//self.ycenter
        self.xcamera = self.xcamera + x_dir
        self.ycamera = self.ycamera + y_dir
        self.xview_scroll(x_dir, "units")
        self.yview_scroll(y_dir, "units")

    def event_edit_maker(self, func):
        def event_func(event):
            if self.edit:
                x, y = event.x, event.y
                x, y = self.xcamera+x, self.ycamera+y
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
    # TODO Set config `default-delay`
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

    def quit(self):
        self.canvas.edit = True
        self.canvas.delete("all")
        self.canvas.cells = []
        self.stop = True
        self.game.clear()

    def set_delay(self, delay):
        self.delay = delay

def set_delay_event(cycle, entry):
    def set_cycle():
        cycle.set_delay(entry.get())
    return set_cycle
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Game of Life")
    
    canvas = LifeGameCanvas(master=root, width=500, height=500, cell_size=(10, 10))
    canvas.pack()

    cycle = Cycle(canvas)
    start_button = tk.Button(master=root, text="Start Cycle")
    start_button.configure(command=cycle.start)
    start_button.pack(side="left")
    refresh_button = tk.Button(master=root, text="Stop Cycle", command=cycle.quit)
    refresh_button.pack(side="left")
    delay_entry = tk.Entry(master=root, width=5)
    # TODO default_delay
    delay_entry.insert(tk.END, "100")
    delay_entry.pack(side="right")
    delay_button = tk.Button(master=root, text="Set delay", command=set_delay_event(cycle, delay_entry))
    delay_button.pack(side="right")
    
    root.mainloop()
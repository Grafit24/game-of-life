"""Entry point to application. Realize GUI and rendering logic."""
from game_of_life import Game
from templates import Singleton
import tkinter as tk
from typing import Callable, Tuple


__author__ = "Sergey Zelenovsky"
__email__ = "zelnovskiygoodman454@gmail.com"


class LifeGameCanvas(tk.Canvas, metaclass=Singleton):
    """Custom canvas class for the Game of Life, that realizing Singleton.

    It contain and render a grid of cell, where one cell is a square 
    cell_size pixels long. Also it update cells on the canvas and 
    realize control related to the canvas: 
        - Camera movement, perform in any mode;
        - Creating cells, perform only in edit mode(edit attr is True);
        - Removing cells, perform only in edit mode(edit attr is True).

    Attributes:
        cell_size : int, is length of every cell's side. One number,
            because cell is square.
        camera_coef : int, coefficient represent camera speed 
            and max camera speed, together. Also max units per tick 
            for camera movement.
        ...
    """
    def __init__(self, cell_size: int, height: int, width: int,
                camera_coef: int, *args, **kwargs)-> None:
        super().__init__(bg="white", height=height, width=width, *args, **kwargs)
        # Additional
        self.width = width
        self.height = height
        self.xcenter, self.ycenter = int(width/2), int(height/2)
        # Rendering
        self.cell_size = cell_size, cell_size
        self.cells = []
        # Camera
        # set unit measurement 
        self.configure(xscrollincrement=1, yscrollincrement=1)
        # TODO Camera move while user it pressed 
        # (use <...Realise> <...Pressed> and var).
        self.bind("<B2-Motion>", self.move_camera)
        self.camera_coef = camera_coef
        self.xcamera, self.ycamera = 0, 0
        # Edit
        self.edit = True
        self.bind("<Button-1>", self.event_edit_maker(self.create_cell))
        self.bind("<Button-3>", self.event_edit_maker(self.remove_cell))

    def get_cells(self)->Tuple[int]:
        """Return tuple of x, y coordinates for cells on the canvas."""
        return tuple(self.cells)

    def render_cells(self, cells):
        """Render new `cells` on the canvas and removing old.
        Cells are list of cell coordinates (x, y)."""
        self.edit = False
        self.delete("all")
        self.cells = list(cells)
        for x, y in cells:
            self.create_cell(x, y)

    def move_camera(self, event: tk.Event)-> None:
        """Move camera by mouse position on the canvas."""
        vector = (-(self.xcenter-event.x), -(self.ycenter-event.y))
        x_dir, y_dir = vector
        x_dir = self.camera_coef*x_dir//self.xcenter
        y_dir = self.camera_coef*y_dir//self.ycenter
        self.xcamera = self.xcamera + x_dir
        self.ycamera = self.ycamera + y_dir
        self.xview_scroll(x_dir, "units")
        self.yview_scroll(y_dir, "units")

    def event_edit_maker(self, func: Callable)-> Callable:
        """Return event function for the mouse-button click.
        Args:
            func : is Callable, that takes cell coordinates.

        Return:
            Callable, func that takes only tk.Event 
            and convert it's pixel coordinates to cell coordinates.
        """
        def event_func(event: tk.Event):
            if self.edit:
                x, y = event.x, event.y
                x, y = self.xcamera+x, self.ycamera+y
                x //= self.cell_size[0]
                y //= self.cell_size[1]
                func(x, y)
        return event_func

    def create_cell(self, x: int, y: int)-> None:
        """Create cell on the canvas by cell coordinates(x, y)."""
        (x0, y0), (x1, y1) = self.convert_coordinates(x, y)
        self.create_rectangle(x0, y0, x1, y1, fill="black", outline="")
        self.cells.append((x, y))

    def remove_cell(self, x: int, y: int)-> None:
        """Remove cell from the canvas by cell coordinates(x, y)."""
        (x0, y0), (x1, y1) = self.convert_coordinates(x, y)
        self.create_rectangle(x0, y0, x1, y1, fill="white", outline="")
        if (x, y) in self.cells:
            self.cells.remove((x, y))

    def convert_coordinates(self, x, y):
        """Convert cell coordinates to pixel coordinates.

        Note. One cell is square, that represented by two points, 
        so coordinates of one cell represented by two pixel coordinates.

        Args:
            x: int, cell coordinate.
            y: int , cell coordinate.

        Return:
            Tuple contains two pixel coordinates (x0, y0), (x1, y1).
        """
        dx, dy = self.cell_size
        return (x*dx, y*dy), ((x+1)*dx, (y+1)*dy)


class Cycle(metaclass=Singleton):
    """Bridge connecting visualization on the canvas and game logic.
    
    It start game use cells on the canvas like initialization cells 
    and disable canvas edit mode.

    Attributes:
        canvas: is LifeGameCanvas for visualization.
        delay: int, delay between updates in ms.
    """
    # TODO Set config `default-delay`
    def __init__(self, canvas: LifeGameCanvas, delay: int=100)-> None:
        self.canvas = canvas
        self._delay = delay
        self.game = Game()
        self.stop = False

    def start(self)-> None:
        self.stop = False
        self.game.init(self.canvas.get_cells())
        self.update()

    def update(self)-> None:
        if not self.stop:
            self.game.update()
            self.canvas.render_cells(self.game.get_cells())
            self.canvas.after(self._delay, self.update)

    def quit(self)-> None:
        self.canvas.edit = True
        self.canvas.delete("all")
        self.canvas.cells = []
        self.stop = True
        self.game.clear()

    def set_delay(self, delay: int)-> None:
        self._delay = delay

def set_delay_event(cycle: Cycle, entry: tk.Entry)-> Callable:
    """Return Callable func for the button command, which 
    sets delay in the Cycle use value in the `entry`.
    """
    def set_delay():
        try:
            entry_value = entry.get()
            cycle.set_delay(int(entry_value))
        except ValueError as e:
            print("The expected delay value was be Integer type.")
    return set_delay
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Game of Life")
    
    canvas = LifeGameCanvas(master=root, width=500, height=500, cell_size=10, camera_coef=3)
    canvas.pack()

    cycle = Cycle(canvas)
    # TODO Unify start and stop button
    # Start button
    start_button = tk.Button(master=root, text="Start Cycle")
    start_button.configure(command=cycle.start)
    start_button.pack(side="left")
    # Refresh button
    refresh_button = tk.Button(master=root, text="Stop Cycle", command=cycle.quit)
    refresh_button.pack(side="left")
    delay_entry = tk.Entry(master=root, width=5)
    # Delay setup
    # TODO default_delay
    delay_entry.insert(tk.END, "100")
    delay_entry.pack(side="right")
    delay_button = tk.Button(master=root, text="Set Delay", command=set_delay_event(cycle, delay_entry))
    delay_button.pack(side="right")
    
    root.mainloop()
# TODO: add a algorithmic maze solver 
import tkinter as tk
import random
import time
from tkinter import messagebox
from tkinter.simpledialog import Dialog
import sys
sys.setrecursionlimit(5000)  # recursive limit increased for large maze (dfs)

# global variables 
start_cell = (-1, -1)   # (row, col)
end_cell = (-1, -1)     # (row, col)
cell_size = None        # calculated later
screen_x = None         # screen resolution
screen_y = None         # screen resolution
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
start_select = False    # selection mode toggles
end_select = False      # same as above 

def record_start_cell(row, col):
    global start_cell
    start_cell = (row, col)
    
def record_end_cell(row, col):
    global end_cell
    end_cell = (row, col)

# get user input for rows and cols count
class two_inputs_prompt(Dialog):
    def body(self, frame):
        tk.Label(frame, text = "Number of Rows:").grid(row = 0, column = 0)
        self.row_entry = tk.Entry(frame)
        self.row_entry.grid(row = 0, column = 1)

        tk.Label(frame, text = "Number of Columns:").grid(row = 1, column = 0)
        self.col_entry = tk.Entry(frame)
        self.col_entry.grid(row = 1, column = 1)

    def apply(self):
        self.result = int(self.row_entry.get()), int(self.col_entry.get())

root = tk.Tk()   # temp root
root.withdraw()  # Hide the main window
# get screen resolution
screen_x = root.winfo_screenwidth()
screen_y = root.winfo_screenheight()
dimensions = two_inputs_prompt(root, "Enter Grid Dimensions")
if dimensions.result:
    print(f"Rows: {dimensions.result[0]}, Columns: {dimensions.result[1]}")
row_size = dimensions.result[0]
col_size = dimensions.result[1]
root.destroy()  # kill temp root

# calculate cell_size
def calculate_cell_size(x, y, length, height):
    y_without_buttons = y - 170  # minus margin needed for the buttons at the bottom

    # Calculate maximum cell size that fits the grid within available space
    actual_x = x // length
    actual_y = y_without_buttons // height

    # Use the smaller dimension to ensure the grid fits both ways
    return min(actual_x, actual_y)

cell_size = calculate_cell_size(screen_x, screen_y, col_size, row_size)

root = tk.Tk()
root.title("Maze Generator")

grid = [[0 for _ in range(col_size)] for _ in range(row_size)]
walls = [[{"top": True, "right": True, "bottom": True, "left": True}
          for _ in range(col_size)] for _ in range(row_size)]

canvas = tk.Canvas(root, width=col_size * cell_size,
                   height=row_size * cell_size)
canvas.pack()

label = tk.Label(root, text="Standby",
                      font=("Arial", 12), fg="red")
label.pack()

# draw the empty grid, first fx called after user input length and width
def initialize_grid():
    canvas.delete("all")    # clear previous grid
    for row in range(row_size):
        for col in range(col_size):
            color_cell(row, col, "white")
    
# helper fx that set start/end cell and return the correct color of the cell 
def set_cell(row, col, flag): 
    grid[row][col] = flag
    if flag == 1:
        color = "blue"
        record_start_cell(row, col)
    elif flag == 2:
        color = "green"
        record_end_cell(row, col)
    return color

# helper fx that reset start/end cell and return white for reset'ed cell
def reset_cell(row, col):
    if grid[row][col] == 1:
        record_start_cell(-1, -1)
    elif grid[row][col] == 2:
        record_end_cell(-1, -1)
    grid[row][col] = 0
    color = "white"
    return color

# fx that handles coloring a cell and updating its surrounding walls
def color_cell(row, col, color):
    # cell coords
    x1 = col * cell_size    # left limit
    x2 = x1 + cell_size     # right limit
    y1 = row * cell_size    # top limit
    y2 = y1 + cell_size     # bottom limit
    canvas.create_rectangle(x1, y1, x2, y2, fill = color, outline = "")
    
    # Draw walls based on current state
    line_width = 2
    
    # doing some overlap calculation for the small uncolored pixel in walls bug
    if walls[row][col]["top"]:
        canvas.create_line(x1 - line_width/2, y1,
                           x2 + line_width/2, y1,
                           fill="black", width=line_width)

    if walls[row][col]["right"]:
        canvas.create_line(x2, y1 - line_width/2,
                           x2, y2 + line_width/2,
                           fill="black", width=line_width)

    if walls[row][col]["bottom"]:
        canvas.create_line(x1 - line_width/2, y2,
                           x2 + line_width/2, y2,
                           fill="black", width=line_width)

    if walls[row][col]["left"]:
        canvas.create_line(x1, y1 - line_width/2,
                           x1, y2 + line_width/2,
                           fill="black", width=line_width)
        
""" parent fx that, given a mouse-click coords and start vs. end flag, handles set/reset, coloring and wall'ing 
    the start/end cell """ 
def update_cell(event, flag):
    # calculate cell clicked
    col = event.x // cell_size    # "col"
    row = event.y // cell_size    # "row"
    
    keep_running = True
    # reset previously set cell first
    # keep_running handles the case of just "deselecting" a cell
    if flag == 1 and start_cell != (-1, -1):
        if start_cell == (row, col):
            keep_running = False
        color_cell(start_cell[0], start_cell[1], "white")
        reset_cell(start_cell[0], start_cell[1])
    elif flag == 2 and end_cell != (-1, -1):
        if end_cell == (row, col):
            keep_running = False
        color_cell(end_cell[0], end_cell[1], "white")
        reset_cell(end_cell[0], end_cell[1])
        
        
    if keep_running and 0 <= row < row_size and 0 <= col < col_size:  # click in bounds check
        if grid[row][col] == 0:
            color = set_cell(row, col, flag)
        else:
            color = reset_cell(row, col)
        color_cell(row, col, color)
    
    print("Starting cell:", start_cell)
    print("Ending cell:", end_cell)
    for row in grid:
        print(row)

# flag: 1 = start cell, 2 = end cell
def start_wrapper():
    global start_select
    global end_select
    start_select = not start_select
    end_select = False  # safeguard
    if start_select:
        root.after(200, lambda: label.config(text="Select a Start Cell", fg="blue"))
        canvas.bind("<Button-1>", lambda event: update_cell(event, 1))
    else:
        root.after(200, lambda: label.config(
            text="Standby", fg="red"))
        canvas.bind("<Button-1>", lambda event: None)  # disable cell selection
    
def end_wrapper(): 
    global start_select
    global end_select
    end_select = not end_select
    start_select = False  # safeguard
    if end_select:
        root.after(200, lambda: label.config(text="Select an End Cell", fg="green"))
        canvas.bind("<Button-1>", lambda event: update_cell(event, 2))
    else:
        root.after(200, lambda: label.config(
            text="Standby", fg="red"))
        canvas.bind("<Button-1>", lambda event: None)  # disable cell selection


# visited grid, default value is false
visited = [[False for _ in range(col_size)] for _ in range(row_size)]
end = False

# NOTE: not ending at end_cell for now
def dfs(prev, current, end):      # dfs algo that destory walls
    # mark cell as visited
    visited[current[0]][current[1]] = True
    if (current == end):
        end = True
        return
    
    if prev:
        # came from top: -top_cell's bottom, -current_cell's top
        if current[0] - prev[0] == 1:
            walls[prev[0]][prev[1]]["bottom"] = False
            walls[current[0]][current[1]]["top"] = False
        # came from bottom: -bottom_cell's top, -current_cell's bottom
        elif current[0] - prev[0] == -1:
            walls[prev[0]][prev[1]]["top"] = False
            walls[current[0]][current[1]]["bottom"] = False
        # came from left: -left_cell's right, -current_cell's left
        elif current[1] - prev[1] == 1:
            walls[prev[0]][prev[1]]["right"] = False
            walls[current[0]][current[1]]["left"] = False
        # came from right: -right_cell's left, -current_cell's right
        elif current[1] - prev[1] == -1:
            walls[prev[0]][prev[1]]["left"] = False
            walls[current[0]][current[1]]["right"] = False
        color_cell(prev[0], prev[1], "white")
        color_cell(current[0], current[1], "white")
            
    # random directions to make it more "maze-like"
    random.shuffle(directions)
    for direction in directions:
        new_row = current[0] + direction[0]
        new_col = current[1] + direction[1]
        # in range check and not visited check
        if end and (0 <= new_row and new_row < row_size) and (0 <= new_col and new_col < col_size) and (visited[new_row][new_col] == False):
            dfs(current, (new_row, new_col), end)

# dfs button wrapper that calls dfs fx
def dfs_wrapper():
    if start_cell == (-1, -1) or end_cell == (-1, -1):
        messagebox.showerror("Error", "Please select start/end cell first!")
    else:
        dfs(None, start_cell, end_cell)
        color_cell(start_cell[0], start_cell[1], "blue")
        color_cell(end_cell[0], end_cell[1], "green")
        root.after(200, lambda: label.config(
            text="Maze created! Start at blue, end at green", fg="green"))
        root.title("Maze")
        canvas.bind("<Button-1>", lambda event: None)
        start_cell_button.pack_forget()
        end_cell_button.pack_forget()
        dfs_button.pack_forget()
        solver_button.pack()


# visual solver for user
path_stack = []

# fx that determine if a move to a cell is valid
def is_valid_move(prev, current):
    # logic:
    # 1. need to be a cell of any valid direction from the prev
    # 2. need to not skip over a wall
    
    # 1.
    direction = (current[0] - prev[0], current[1] - prev[1])
    if (abs(direction[0] + abs(direction[1]))) != 1:
        return False

    # 2.
    # came from above
    if direction == (1, 0):
        return not (walls[prev[0]][prev[1]]["bottom"]) and not (walls[current[0]][current[1]]["top"])
    # came from below
    if direction == (-1, 0):
        return not (walls[prev[0]][prev[1]]["top"]) and not (walls[current[0]][current[1]]["bottom"])
    # came from the left
    if direction == (0, 1):
        return not (walls[prev[0]][prev[1]]["right"]) and not (walls[current[0]][current[1]]["left"])
    # came from the right
    if direction == (0, -1):
        return not (walls[prev[0]][prev[1]]["left"]) and not (walls[current[0]][current[1]]["right"])

# fx to create a path
# path_cell has value 5
def create_path(current):
    if (len(path_stack) == 0):
        path_stack.append(start_cell)
    prev = path_stack[-1]
    
    if current == end_cell:
        if abs(end_cell[0] - prev[0]) + abs(end_cell[1] - prev[1]) == 1:
            messagebox.showinfo("Maze Solver", "You reached the end cell!")
            return
        messagebox.showinfo("Maze Solver", "Hey don't cheat now...")

    if current not in path_stack and is_valid_move(prev, current): 
        path_stack.append(current)
        color_cell(current[0], current[1], "blue")

# helper fxs that select a cell when given coords of cells dragged over/clicked on
def on_drag(event):
    col = event.x // cell_size
    row = event.y // cell_size
    if 0 <= row < row_size and 0 <= col < col_size: 
        create_path((row, col))

def on_click(event):
    col = event.x // cell_size
    row = event.y // cell_size
    if 0 <= row < row_size and 0 <= col < col_size:
        create_path((row, col))

# helper fxs that deselect a cell when given coords of right click 
def backtrack(event):
    col = event.x // cell_size
    row = event.y // cell_size
    # only allow backtracking the last step
    if len(path_stack) != 0 and path_stack[-1] == (row, col):
        path_stack.pop(-1)
        color_cell(row, col, "white")  # Reset cell color

# maze solver parent fx
def solver_wrapper():
    canvas.bind("<B1-Motion>", on_drag)     # left mouse button drag for path
    canvas.bind("<Button-1>", on_click)     # left mouse button click for path
    canvas.bind("<Button-3>", backtrack)    # Right mouse button click for backtracking
    messagebox.showinfo(
        "Maze Solver", "Drag or click to create a path. Right-click to backtrack. Good luck!")
    root.after(200, lambda: label.config(
        text="Drag/click for path, right click for backtracking. End at green", fg="green"))

    
initialize_grid()

# buttons
start_cell_button = tk.Button(root, text="Select a starting cell",
                            command=start_wrapper)
end_cell_button = tk.Button(root, text="Select an ending cell",
                            command=end_wrapper)
dfs_button = tk.Button(root, text="Begin Maze Construction",
                            command=dfs_wrapper)
solver_button = tk.Button(
    root, text="Let me solve it!", command=solver_wrapper)

start_cell_button.pack()
end_cell_button.pack()
dfs_button.pack()

root.mainloop()

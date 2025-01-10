# TODO: give user a visual solver

import tkinter as tk
import random
import time
from tkinter import simpledialog, messagebox
from collections import defaultdict

# from dfs import dfs     # dfs algo

start_cell = (-1, -1)   # (row, col)
end_cell = (-1, -1)     # (row, col)
def record_start_cell(row, col):
    global start_cell
    start_cell = (row, col)
    
def record_end_cell(row, col):
    global end_cell
    end_cell = (row, col)

row_size = simpledialog.askinteger("Input", "Enter number of rows:")
col_size = simpledialog.askinteger("Input", "Enter number of columns:")

grid = [[0 for _ in range(col_size)] for _ in range(row_size)]
walls = [[{"top": True, "right": True, "bottom": True, "left": True}
          for _ in range(col_size)] for _ in range(row_size)]

cell_size = 25
root = tk.Tk()
root.title("Grid")
canvas = tk.Canvas(root, width=col_size * cell_size,
                   height=row_size * cell_size)
canvas.pack()

# flags to enable cell selection 
start_select = False
end_select = False
label = tk.Label(root, text="Standby",
                      font=("Arial", 12), fg="red")
label.pack()

def initialize_grid():
    canvas.delete("all")    # clear previous grid
    for row in range(row_size):
        for col in range(col_size):
            color_cell(row, col, "white")
    
def set_cell(row, col, flag): 
    grid[row][col] = flag
    if flag == 1:
        color = "blue"
        record_start_cell(row, col)
    elif flag == 2:
        color = "green"
        record_end_cell(row, col)
    return color

def reset_cell(row, col):
    if grid[row][col] == 1:
        record_start_cell(-1, -1)
    elif grid[row][col] == 2:
        record_end_cell(-1, -1)
    grid[row][col] = 0
    color = "white"
    return color

def color_cell(row, col, color):
    # cell coords
    x1 = col * cell_size    # left limit
    x2 = x1 + cell_size     # right limit
    y1 = row * cell_size    # top limit
    y2 = y1 + cell_size     # bottom limit
    canvas.create_rectangle(x1, y1, x2, y2, fill = color, outline = "")
    
    line_width = 2
    overlap = 1

    if walls[row][col]["top"]:
        canvas.create_line(x1, y1, x2, y1, fill="black", width=line_width)
    if walls[row][col]["right"]:
        canvas.create_line(x2 - overlap, y1, x2 - overlap, y2, fill="black", width=line_width)
    if walls[row][col]["bottom"]:
        canvas.create_line(x1, y2 - overlap, x2, y2 - overlap, fill="black", width=line_width)
    if walls[row][col]["left"]:
        canvas.create_line(x1, y1, x1, y2, fill="black", width=line_width)

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


directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
# visited grid, default value is false
visited = [[False for _ in range(col_size)] for _ in range(row_size)]

# NOTE: not ending at end_cell for now
def dfs(prev, current, end):      # dfs algo that destory walls
    # mark cell as visited
    visited[current[0]][current[1]] = True
    
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
        if (0 <= new_row and new_row < row_size) and (0 <= new_col and new_col < col_size) and (visited[new_row][new_col] == False):
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
    canvas.bind("<Button-1>", lambda event: None)
    start_cell_button.pack_forget()
    end_cell_button.pack_forget()
    dfs_button.pack_forget()
    
initialize_grid()

# buttons
start_cell_button = tk.Button(root, text="Select a starting cell",
                            command=start_wrapper)
end_cell_button = tk.Button(root, text="Select an ending cell",
                            command=end_wrapper)
dfs_button = tk.Button(root, text="Begin Maze Construction",
                            command=dfs_wrapper)

start_cell_button.pack()
end_cell_button.pack()
dfs_button.pack()

root.mainloop()

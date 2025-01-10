# TODO: give user options to start the maze construction:
# see the deconstruction of walls or not

# temp having all functon in this file

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

g_size = simpledialog.askinteger("Input", "Enter width/length:")
grid = [[0 for _ in range(g_size)] for _ in range(g_size)]
walls = [[{"top": True, "right": True, "bottom": True, "left": True}
    for _ in range(g_size)] for _ in range(g_size)]

cell_size = 35
root = tk.Tk()
root.title("Grid")
canvas = tk.Canvas(root, width=g_size * cell_size, height=g_size * cell_size)
canvas.pack()

# flags to enable cell selection 
start_select = False
end_select = False
label = tk.Label(root, text="Standby",
                      font=("Arial", 12), fg="red")
label.pack()

"""
# text showing starting and ending cell coords
start_cell_coords = canvas.create_text(
    g_size * cell_size // 2, g_size * cell_size + 20, text="Not Selected", font=("Arial", 30), fill="blue")

end_cell_coords = canvas.create_text(
    100, 70, text="Not Selected", font=("Arial", 14), fill="green")
"""

def initialize_grid():
    canvas.delete("all")    # clear previous grid
    for row in range(g_size):
        for col in range(g_size):
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
        
    if keep_running and 0 <= row < g_size and 0 <= col < g_size:  # click in bounds check
        if grid[row][col] == 0:
            color = set_cell(row, col, flag)
        else:
            color = reset_cell(row, col)
        color_cell(row, col, color)
    
    print("Starting cell:", start_cell)
    print("Ending cell:", end_cell)
    for row in grid:
        print(row)
        
def update_wall(prev, current):
    pass

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



"""
# just a test to remove top wall 
# note that cell's top wall is removed, not the cell above's bottom wall
def remove_wall(event):
    # calculate cell clicked
    col = event.x // cell_size
    row = event.y // cell_size
    print("2. x", col, "y", row)
    
    if 0 <= row < g_size and 0 <= col < g_size:
        if (walls[row][col]["top"]):
            walls[row][col]["top"] = False
        else: 
            walls[row][col]["top"] = True
        draw_grid()
"""    

initialize_grid()

# buttons
start_cell_button = tk.Button(root, text="Select a starting cell",
                            command=start_wrapper)
end_cell_button = tk.Button(root, text="Select an ending cell",
                            command=end_wrapper)


start_cell_button.pack()
end_cell_button.pack()

root.mainloop()

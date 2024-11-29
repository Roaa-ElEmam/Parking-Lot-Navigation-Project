import tkinter as tk
from tkinter import messagebox
from collections import deque
import time
from PIL import Image, ImageTk

GRID_ROWS = 10
GRID_COLS = 10
CELL_SIZE = 40

EMPTY_COLOR = "white"
OBSTACLE_COLOR = "black"
START_COLOR = "green"
GOAL_COLOR = "blue"
VISITED_COLOR = "light gray"
PATH_COLOR = "yellow"
CAR_COLOR = "orange"

grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
entrance = (0, 0)
exit_point = entrance
parking_spots = [(5, 4), (8, 9), (9, 2)]

obstacles = [
    (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7),
    (2, 3), (3, 3), (3, 4), (4, 4), (5, 5), 
    (5, 6), (6, 6), (6, 3), (7, 5), (8, 5), (8, 6), 
    (8, 7), (9, 6), (4, 2), (6, 2), (7, 2), (2, 8), 
    (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)
]

# Initialize grid with obstacles and parking spots
for (r, c) in obstacles:
    grid[r][c] = 1  # Mark as obstacles

# Tkinter setup
window = tk.Tk()
window.title("BFS Parking Lot Navigation")

canvas = tk.Canvas(window, width=GRID_COLS * CELL_SIZE, height=GRID_ROWS * CELL_SIZE)
canvas.pack()

car_image = Image.open("RedCarV.png")
car_image = car_image.resize((CELL_SIZE, CELL_SIZE))  # Resize image to fit the cell size
car_image_up = car_image.rotate(180)
car_image_down = car_image
car_image_left =  car_image.rotate(-90)
car_image_right =  car_image.rotate(90)  # Original image pointing right

# Convert to Tkinter images
car_tk_image_up = ImageTk.PhotoImage(car_image_up)
car_tk_image_down = ImageTk.PhotoImage(car_image_down)
car_tk_image_left = ImageTk.PhotoImage(car_image_left)
car_tk_image_right = ImageTk.PhotoImage(car_image_right)

# Draw the grid
def draw_grid():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            color = EMPTY_COLOR
            if grid[row][col] == 1:
                color = OBSTACLE_COLOR
            elif (row, col) == entrance:
                color = START_COLOR
            elif (row, col) in parking_spots:
                color = GOAL_COLOR

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

# Update cell color
def update_cell(row, col, color):
    x1 = col * CELL_SIZE
    y1 = row * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
    window.update()


def bfs(start, goals):
    queue = deque([(start, [])])  # (current_position, path)
    visited = set()
    visited.add(start)
    nodes_visited = 0  # To calculate space complexity

    while queue:
        (current, path) = queue.popleft()
        current_row, current_col = current
        nodes_visited += 1  # Increment nodes visited

        # Visualize the visit with a slower speed (0.15s delay)
        if current != start and current not in goals:
            update_cell(current_row, current_col, VISITED_COLOR)
            time.sleep(0.15)

        # Goal found, choose the closest parking spot
        if current in goals:
            return current, path, nodes_visited  # Return parking spot, path, and nodes visited

        # Explore neighbors
        for (d_row, d_col) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current_row + d_row, current_col + d_col)

            if (0 <= neighbor[0] < GRID_ROWS and 0 <= neighbor[1] < GRID_COLS and
                neighbor not in visited and grid[neighbor[0]][neighbor[1]] == 0):

                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None, [], nodes_visited  # If no goal is found


def move_car_along_path(path):
    car_image_id = None
    final_row, final_col = path[-1]
    for (row, col) in path:
        update_cell(row, col, CAR_COLOR)

    for i in range(len(path) - 1):
        (current_row, current_col) = path[i]
        (next_row, next_col) = path[i + 1]

        # Determine the direction of movement
        if next_row < current_row:  # Moving up
            car_tk_image = car_tk_image_up
        elif next_row > current_row:  # Moving down
            car_tk_image = car_tk_image_down
        elif next_col < current_col:  # Moving left
            car_tk_image = car_tk_image_left
        elif next_col > current_col:  # Moving right
            car_tk_image = car_tk_image_right

        # Calculate the top-left corner of the cell
        x1 = current_col * CELL_SIZE
        y1 = current_row * CELL_SIZE

        # Delete the previous car image if it exists
        if car_image_id is not None:
            canvas.delete(car_image_id)

        # Create the car image at the correct position and orientation
        car_image_id = canvas.create_image(x1 + CELL_SIZE // 2, y1 + CELL_SIZE // 2, image=car_tk_image)

        time.sleep(0.1)  # Slow delay to visualize the car movement
        window.update()  # Update the window to reflect the movement
        # Show the car at the final position (last point in the path)
        if car_image_id is not None:
            canvas.delete(car_image_id)  # Delete the previous image to avoid duplicates
            time.sleep(0.1)
            
    x1 = final_col * CELL_SIZE
    y1 = final_row * CELL_SIZE  

    # Place the car at the final position
    canvas.create_image(x1 + CELL_SIZE // 2, y1 + CELL_SIZE // 2, image=car_tk_image)

# Display Time and Space Complexity in a popup window
def display_complexity(search_type, time_complexity, space_complexity):
    message = f"{search_type} Search Completed!\n\n"
    message += f"Time Complexity (Steps Taken): {time_complexity}\n"
    message += f"Space Complexity (Nodes Visited): {space_complexity}\n"
    messagebox.showinfo(f"{search_type} Complexity", message)

def start_bfs_to_parking():
    draw_grid()
    global parking_spot, parking_path, nodes_visited_to_parking
    parking_spot, parking_path, nodes_visited_to_parking = bfs(entrance, parking_spots)
    
    if parking_spot:
        print(f"Parking Spot Found at: {parking_spot}")
        move_car_along_path(parking_path)  # Visualize car movement to the parking spot
        start_exit_button.config(state="normal")  # Enable the exit button after finding a parking spot
        display_complexity("Parking Spot", len(parking_path), nodes_visited_to_parking)
    else:
        print("No Parking Spot Available!")

def start_bfs_to_exit():
    if parking_spot:
        draw_grid()
        update_cell(parking_spot[0], parking_spot[1], PATH_COLOR)  # Mark the current parking spot
        _, path_to_exit, nodes_visited_to_exit = bfs(parking_spot, [exit_point])
        
        if path_to_exit:
            move_car_along_path(path_to_exit)  # Visualize car movement back to the entrance
            print("Path to Exit Found!")
            display_complexity("Exit", len(path_to_exit), nodes_visited_to_exit)
        else:
            print("No Path to Exit!")
    else:
        print("No Parking Spot Selected.")

draw_grid()

start_button = tk.Button(window, text="Start Search to Parking Spot", command=start_bfs_to_parking)
start_button.pack()

start_exit_button = tk.Button(window, text="Start Search to Exit", command=start_bfs_to_exit, state="disabled")
start_exit_button.pack()

window.mainloop()
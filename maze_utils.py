import random
from pgl import GWindow, GRect, GOval

CELL_SIZE = 50

def generate_maze(rows, cols):
    # 1. Initialize with all walls (1 = wall, 0 = path)
    # We use odd numbers for rows/cols to ensure we have "wall" dividers
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    
    def carve_path(r, c):
        maze[r][c] = 0 # Mark current cell as path
        
        # Randomize directions to keep the maze "organic"
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Check if the new cell is within bounds and still a wall
            if 0 < nr < rows-1 and 0 < nc < cols-1 and maze[nr][nc] == 1:
                # Remove the wall between the current cell and the new cell
                maze[r + dr//2][c + dc//2] = 0
                carve_path(nr, nc)

    # Start carving from (1, 1)
    carve_path(1, 1)

   
    # Surround the island with a "moat" of walls
    # We ensure these stay as walls (1) to disconnect the center
    for dr in range(1, rows-1):
        for dc in range(1, cols-1):
            if dr == 1 or dr == rows - 2 or dc == 1 or dc == cols - 2:
                maze[dr][dc] = 0

    # Grab an exit from available spae in the interior
    possible_exit_locs = []
    for dr in range(2, rows-2):
        for dc in range(2, cols-2):
            if maze[dr][dc] == 0:
                possible_exit_locs.append((dr, dc))
    exit_at = random.choice(possible_exit_locs)
    
    # 2. Finalize: Convert to your string format and add Start/Exit
    str_maze = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if r == 1 and c == 1: row.append("S")
            elif r == exit_at[0] and c == exit_at[1]: row.append("E")
            else: row.append("X" if maze[r][c] == 1 else ".")
        str_maze.append(row)
        
    return str_maze

def display(maze):
    for row in maze:
        print("".join(row))

def visualize(maze):
    height = len(maze)
    width = len(maze[0])


    gw = GWindow(width*CELL_SIZE, height*CELL_SIZE)
    marker = GOval(CELL_SIZE*.75, CELL_SIZE * .75)
    marker.set_filled(True)
    marker.set_fill_color('orange')
    gw.add(marker)

    def place_marker(r,c):
        x = (c + 0.5) * CELL_SIZE - marker.get_width() / 2
        y = (r + 0.5) * CELL_SIZE - marker.get_height() / 2
        marker.set_location(x, y)
        visited = GRect(c * CELL_SIZE, r * CELL_SIZE, 0.1 * CELL_SIZE, 0.1 * CELL_SIZE)
        visited.set_filled(True)
        visited.set_fill_color('lightgray')
        gw.add(visited)

    for r in range(height):
        for c in range(width):
            rect = GRect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[r][c] == 'S':
                rect.set_filled(True)
                rect.set_fill_color('green')
                place_marker(r,c)
                print(f"[{r}][{c}]")
            elif maze[r][c] == 'E':
                rect.set_filled(True)
                rect.set_fill_color('red')
            elif maze[r][c] == "X":
                rect.set_filled(True)
            gw.add(rect)
            rect.send_to_back()

    def click_move(e):
        mx, my = e.get_x(), e.get_y()
        r, c = my // CELL_SIZE, mx // CELL_SIZE
        print(f"[{r}][{c}]")
        place_marker(r,c)

    gw.add_event_listener('click', click_move)



if __name__ == '__main__':
# Best used with odd numbers (e.g., 15x15, 21x21)
    real_maze = generate_maze(7, 7)
    # display(real_maze)
    visualize(real_maze)

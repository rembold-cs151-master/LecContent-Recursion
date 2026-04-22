from maze_utils import generate_maze, visualize


def solve(r, c, maze):
    # BASE CASE 1: Success! Return the last step of the path.
    if maze[r][c] == "E":
        return [(r, c)]
    
    # BASE CASE 2: Illegal or pointless moves
    if maze[r][c] == 'X' or maze[r][c] == "V":
        return None

    # Mark as visited to prevent cycling
    maze[r][c] = "V"

    # Recursive step: Ask the neighbors (down, up, right, left)
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        result = solve(r + dr, c + dc, maze)
        
        # If result is not None, it means this neighbor found the exit!
        if result is not None:
            # We add our current position to the path and pass it up the chain
            return [(r, c)] + result

    # 4. If the loop finishes and no neighbor found a path...
    return None

if __name__ == '__main__':
    SIZE = 7
    maze = generate_maze(SIZE, SIZE)
    visualize(maze)

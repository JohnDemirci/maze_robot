
import copy
import sys
from collections import deque

def goal_check(maze, position):
    return maze[position[0]][position[1]] == "D"

def end_game(path, position):
    print("FOUND THE DIAMOND AT", position[0], position[1])
    path.append(position[1])
    print(path)
    sys.exit(0)

"""
changing the position based on the direction we are heading
"""
def position_change(pos):
    if pos[1] == "l":
        new_pos = (pos[0][0], pos[0][1]-1)
        pos = (new_pos, "l")
    elif pos[1] == "r":
        new_pos = (pos[0][0], pos[0][1]+1)
        pos = (new_pos, "r")
    elif pos[1] == "u":
        new_pos = (pos[0][0]-1, pos[0][1])
        pos = (new_pos, "u")
    elif pos[1] == "d":
        new_pos = (pos[0][0]+1, pos[0][1])
        pos = (new_pos, "d")
    return pos


def find_value(maze, val):
    for outer in range(9):
        for inner in range(9):
            if maze[outer][inner] == val:
                return (outer, inner)

"""
successor function

move and analyze the surroundings
append the fringe
"""
def get_actions(current, visited):
    maze = copy.deepcopy(fringe[0][0])
    path = copy.deepcopy(fringe[0][1])
    left = (current, "l")
    right = (current, "r")
    up = (current, "u")
    down = (current, "d")
    directions = [left, down, right, up]
    new_list = []
    fringe.popleft()
    for direction in directions:
        val = goto_direction(maze, direction, visited, path)
        if val != None:
            new_path = copy.deepcopy(path)
            new_path.append(direction[1])
            fringe.appendleft( (val, new_path) )
    
"""
function that moves to a direction
"""
def goto_direction(maze, direction, visited, path):
    return_maze = go_x(maze, direction, visited, path)
    return return_maze

"""
moves to the given direction until hits a wall or finds the goal
"""
def go_x(maze, position, visited, path):
    robot_location = find_value(maze, "R")
    previous_pos = None
    while maze[position[0][0]][position[0][1]] != "1":
        previous_pos = position[:]
        if goal_check(maze, position[0]):
            end_game(path, position)
        position = position_change(position)
        if maze[position[0][0]][position[0][1]] == "1":
            position = previous_pos[:]
            break
    new_maze = copy.deepcopy(maze)
    new_maze[robot_location[0]][robot_location[1]] = "0"
    new_maze[position[0][0]][position[0][1]] = "R"
    if new_maze not in visited:
        visited.append(new_maze)
        return new_maze
    else:
        return None

def main():
    labyrinth = [
        ["1", "1", "1", "1", "1", "1", "1", "1", "1"],
        ["1", "0", "0", "0", "1", "0", "0", "R", "1"],
        ["1", "0", "0", "0", "1", "0", "0", "0", "1"],
        ["1", "0", "0", "0", "0", "0", "0", "0", "1"],
        ["1", "0", "0", "0", "0", "1", "0", "0", "1"],
        ["1", "1", "1", "0", "0", "1", "0", "0", "1"],
        ["1", "1", "1", "0", "0", "1", "1", "1", "1"],
        ["1", "1", "0", "0", "0", "0", "0", "D", "1"],
        ["1", "1", "1", "1", "1", "1", "1", "1", "1"]]
    start = copy.deepcopy(labyrinth)
    visited_walls = []
    path = []
    visited_walls.append(start)
    fringe.append((start, path))
    robot_location = find_value(start, "R")

    while len(fringe):
        get_actions(robot_location, visited_walls)
        try:
            robot_location = find_value(fringe[0][0], "R")
        except:
            print("COULD NOT FIND THE DIAMOND")
            break


if __name__ == "__main__":
    fringe = deque()
    main()

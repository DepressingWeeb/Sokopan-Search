import ctypes
import multiprocessing
import os

from A_star import AStar
from UCS import UCS
from bfs import BFS
from dfs import DFS


def sokoban_pushed_weights(board, weight_list, solution):
    stones_coord_and_weight = []
    w_idx = 0
    n_rows = len(board)
    n_cols = len(board[0])
    char_coord = None
    for i in range(n_rows):
        for j in range(n_cols):
            if board[i][j] == '$':
                stones_coord_and_weight.append((i, j, weight_list[w_idx]))
                w_idx += 1
            elif board[i][j] == '@':
                char_coord = (i, j)
    # Initialize the character's starting position and the stone positions/weights
    char_x, char_y = char_coord
    stones = {(x, y): w for x, y, w in stones_coord_and_weight}

    # Map directions to coordinate changes
    direction_map = {
        'u': (-1, 0), 'U': (-1, 0),
        'd': (1, 0), 'D': (1, 0),
        'l': (0, -1), 'L': (0, -1),
        'r': (0, 1), 'R': (0, 1),
    }

    # List to store cumulative weight pushed at each step
    weights_pushed = []
    cumulative_weight = 0  # Keep track of the cumulative weight pushed

    # Process each move in the solution
    for move in solution:
        dx, dy = direction_map[move]
        cumulative_weight += 1
        if move.islower():  # Character moves without pushing a stone
            # Update character position
            char_x += dx
            char_y += dy
            weights_pushed.append(cumulative_weight)  # No weight added, just append the current cumulative weight
        else:  # Character pushes a stone
            # Calculate stone's current position (adjacent in the direction of push)
            stone_x = char_x + dx
            stone_y = char_y + dy

            # Calculate the stone's new position after the push
            new_stone_x = stone_x + dx
            new_stone_y = stone_y + dy

            # Get the weight of the stone at the current position
            if (stone_x, stone_y) in stones:
                weight = stones[(stone_x, stone_y)]
                cumulative_weight += weight  # Add the stone's weight to the cumulative weight
                weights_pushed.append(cumulative_weight)

                # Move the stone to its new position
                stones.pop((stone_x, stone_y))
                stones[(new_stone_x, new_stone_y)] = weight

                # Update character's position (character moves into the pushed stone's position)
                char_x += dx
                char_y += dy
            else:
                weights_pushed.append(
                    cumulative_weight)  # Append the current cumulative weight if no stone is pushed

    return weights_pushed

def input_txt_file(file_path):
    with open(file_path,'r') as f:
        lines = f.readlines()
        weight_list = list(map(int,lines[0].strip().split(' ')))
        max_width = max([len(line.rstrip()) for line in lines[1:]])
        board = []
        for line in lines[1:]:
            line = line.rstrip()
            while len(line)<max_width:
                line+= ' '
            line_split = [char for char in line]
            board.append(line_split)
    return board,weight_list

def to_output(path_to_input_txt):

    board,weight_list = input_txt_file(path_to_input_txt)
    time_taken = multiprocessing.Value('d', 0)
    node = multiprocessing.Value('i', 0)
    path = multiprocessing.Array(ctypes.c_char, 10000)
    stop_signal = multiprocessing.Event()
    f = open(f'out/output_for_{os.path.basename(path_to_input_txt)}.txt','w')
    def to_str(algo_name,res):
        path_out, node_count_out, time_taken_out, memory_out= res
        weight_pushed = -1
        if path_out != 'No solution found':
            weight_pushed=sokoban_pushed_weights(board,weight_list,path_out)[-1]
        f.write(algo_name+'\n')
        f.write(f'Steps: {len(path_out)}, Weight: {weight_pushed}, Node: {node_count_out}, Time (ms): {time_taken_out*1000}, Memory (MB): {memory_out}\n')
        f.write(path_out+'\n')


    a_star_instance = AStar(board, weight_list)
    res1 = a_star_instance.A_star(time_taken, node, path, stop_signal)
    ucs_instance = UCS(board,weight_list)
    res2 = ucs_instance.UCS(time_taken, node, path, stop_signal)
    bfs_instance = BFS(board)
    res3 = bfs_instance.BFS(time_taken, node, path, stop_signal)
    dfs_instance = DFS(board)
    res4 = dfs_instance.DFS(time_taken, node, path, stop_signal)
    to_str('BFS',res3)
    to_str('DFS',res4)
    to_str('UCS',res2)
    to_str('A*',res1)
    f.close()

def get_all_output(path_to_level_folder):
    file_paths = os.listdir(path_to_level_folder)
    for path in file_paths:
        to_output(os.path.join(path_to_level_folder,path))
        print(f'Done {path}')


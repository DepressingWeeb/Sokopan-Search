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

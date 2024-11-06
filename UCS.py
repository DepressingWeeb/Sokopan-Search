
from collections import deque
from queue import PriorityQueue
class UCS:
    def __init__(self, board,weight_list):
        self.board_begin = board
        self.board = board
        self.n_rows = len(board)
        self.n_cols = len(board[0])
        self.weight_list = weight_list
        self.walls_coord_set = set()  # Contains coordinates of walls, cannot be changed
        self.target = []  # Contains the switch coordinates sorted, cannot be changed
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if board[i][j] == '.':
                    self.target.append((i, j))
                elif board[i][j] == '#':
                    self.walls_coord_set.add((i, j))
        self.target.sort()

    def can_push(self, push_dir, char_coord, stones_coord, walls_coord_set):
        # Determine the direction vector based on push_dir
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)][push_dir]
        char_x, char_y = char_coord
        stone_x, stone_y = char_x + direction[0], char_y + direction[1]
        next_x, next_y = stone_x + direction[0], stone_y + direction[1]

        # Check if the stone's current position is in the stones_coord
        if (stone_x, stone_y) not in stones_coord:
            return False

        # Check if the next position is out of bounds or blocked
        if not (0 <= next_x < self.n_rows and 0 <= next_y < self.n_cols):
            return False
        if (next_x, next_y) in walls_coord_set or (next_x, next_y) in stones_coord:
            return False

        # Valid push
        return True

    def can_move(self, move_dir, char_coord, walls_coord_set):
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)][move_dir]
        char_x, char_y = char_coord
        next_x, next_y = char_x + direction[0], char_y + direction[1]
        if not (0 <= next_x < self.n_rows and 0 <= next_y < self.n_cols):
            return False
        return (next_x, next_y) not in walls_coord_set

    def is_move_or_push(self, dir, char_coord, stones_coord):
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)][dir]
        char_x, char_y = char_coord
        next_x, next_y = char_x + direction[0], char_y + direction[1]

        return (next_x, next_y) not in stones_coord
    def UCS(self):
        q = PriorityQueue()
        visited = set()
        char_coord = (0, 0)
        node_count = 0
        stones_weight_and_coord = []
        w_idx = 0
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.board[i][j] == '$':
                    stones_weight_and_coord.append((i, j,self.weight_list[w_idx]))
                    w_idx+=1
                elif self.board[i][j] == '@':
                    char_coord = (i, j)

        # Each state: (g(n),current char_coord, (stone_x,stone_y,weight), action path)
        q.put((0,char_coord, stones_weight_and_coord, ""))
        while q.qsize()>0:
            g_n,curr_char_coord, curr_stones_weight_and_coord, path = q.get()
            #extract the stone coord list only
            curr_stones_coord = [(wc[0],wc[1]) for wc in curr_stones_weight_and_coord]
            # Check if all stones are on the switches
            if sorted(curr_stones_coord) == self.target:
                return (path,node_count)  # Return the action path
            if (curr_char_coord, tuple(curr_stones_weight_and_coord)) in visited:
                continue
            node_count += 1
            if node_count % 100000 == 0:
                print(node_count)
            visited.add((curr_char_coord, tuple(curr_stones_weight_and_coord)))
            # Try all 4 possible directions: Up, Down, Left, Right
            for direction in range(4):
                if self.is_move_or_push(direction, curr_char_coord, curr_stones_coord):
                    # Move action
                    if self.can_move(direction, curr_char_coord, self.walls_coord_set):
                        new_char_coord = (curr_char_coord[0] + [-1, 1, 0, 0][direction],
                                          curr_char_coord[1] + [0, 0, -1, 1][direction])
                        q.put((g_n+1,new_char_coord, curr_stones_weight_and_coord, path + "udlr"[direction]))
                else:
                    #print('Push')
                    # Push action
                    if self.can_push(direction, curr_char_coord, curr_stones_coord, self.walls_coord_set):
                        # Perform the push
                        new_char_coord = (curr_char_coord[0] + [-1, 1, 0, 0][direction],
                                          curr_char_coord[1] + [0, 0, -1, 1][direction])
                        new_stones_weight_and_coord = list(curr_stones_weight_and_coord)
                        new_stone_pos_x = new_char_coord[0] + [-1, 1, 0, 0][direction]
                        new_stone_pos_y = new_char_coord[1] + [0, 0, -1, 1][direction]
                        idx = -1
                        for i in range(len(curr_stones_weight_and_coord)):
                            wc = curr_stones_weight_and_coord[i]
                            if (wc[0], wc[1]) == new_char_coord:
                                idx = i
                                break
                        if idx == -1:
                            raise RuntimeError()
                        weight = curr_stones_weight_and_coord[idx][2]
                        new_stones_weight_and_coord[idx] = (new_stone_pos_x,new_stone_pos_y,weight)
                        q.put((g_n+weight + 1,new_char_coord, new_stones_weight_and_coord, path + "UDLR"[direction]))
                        #visited.add((new_char_coord, tuple(new_stones_coord)))

        return ("No solution found",node_count)  # If no solution is found
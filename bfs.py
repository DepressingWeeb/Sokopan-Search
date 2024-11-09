import time
from collections import deque

import psutil


class BFS:
    def __init__(self, board):
        self.board_begin = board
        self.board = board
        self.n_rows = len(board)
        self.n_cols = len(board[0])
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
    def BFS(self,time_taken,node_count_shared,path_shared,stop_signal):
        process = psutil.Process()
        memory_start = process.memory_info().rss / (1024 * 1024)
        start_time = time.time()
        q = deque()
        visited = set()
        char_coord = (0, 0)
        node_count = 0
        stones_coord = []
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.board[i][j] == '$':
                    stones_coord.append((i, j))
                elif self.board[i][j] == '@':
                    char_coord = (i, j)

        # Each state: (current char_coord, stone positions, action path)
        q.append((char_coord, stones_coord, ""))

        while q:

            curr_char_coord, curr_stones_coord, path = q.popleft()
            # Check if all stones are on the switches

            if sorted(curr_stones_coord) == self.target:
                node_count_shared.value = node_count
                path_shared.value = path.encode()
                time_taken.value = time.time() - start_time
                memory = process.memory_info().rss / (1024 * 1024) - memory_start
                return (path, node_count, time_taken.value, memory)
            if (curr_char_coord, tuple(curr_stones_coord)) in visited:
                continue
            visited.add((curr_char_coord, tuple(curr_stones_coord)))
            node_count += 1
            if node_count % 100 == 0:
                node_count_shared.value = node_count
                time_taken.value = time.time() - start_time
                if stop_signal.is_set():
                    break
            # Try all 4 possible directions: Up, Down, Left, Right
            for direction in range(4):
                if self.is_move_or_push(direction, curr_char_coord, curr_stones_coord):
                    # Move action
                    if self.can_move(direction, curr_char_coord, self.walls_coord_set):
                        new_char_coord = (curr_char_coord[0] + [-1, 1, 0, 0][direction],
                                          curr_char_coord[1] + [0, 0, -1, 1][direction])
                        q.append((new_char_coord, curr_stones_coord, path + "udlr"[direction]))
                else:
                    #print('Push')
                    # Push action
                    if self.can_push(direction, curr_char_coord, curr_stones_coord, self.walls_coord_set):
                        # Perform the push
                        new_char_coord = (curr_char_coord[0] + [-1, 1, 0, 0][direction],
                                          curr_char_coord[1] + [0, 0, -1, 1][direction])
                        new_stones_coord = list(curr_stones_coord)
                        new_stone_pos = (new_char_coord[0] + [-1, 1, 0, 0][direction],
                                         new_char_coord[1] + [0, 0, -1, 1][direction])
                        new_stones_coord.remove((new_char_coord[0], new_char_coord[1]))
                        new_stones_coord.append(new_stone_pos)
                        q.append((new_char_coord, new_stones_coord, path + "UDLR"[direction]))
                        #visited.add((new_char_coord, tuple(new_stones_coord)))
        node_count_shared.value = node_count
        path_shared.value = "No solution found".encode()
        time_taken.value = time.time() - start_time
        memory = process.memory_info().rss / (1024 * 1024) - memory_start
        return ("No solution found",node_count, time_taken.value, memory)  # If no solution is found
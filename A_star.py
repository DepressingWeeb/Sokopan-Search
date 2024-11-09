import time
from collections import deque
from queue import PriorityQueue

import numpy as np
import psutil
import scipy
class AStar:
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
        self.preprocess()


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
    def can_pull(self, pull_dir, stone_coord, walls_coord_set):
        # Determine the direction vector based on push_dir
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)][pull_dir]
        stone_x,stone_y = stone_coord[0],stone_coord[1]
        char_x, char_y = stone_x + direction[0], stone_y + direction[1]
        next_x, next_y = char_x + direction[0], char_y + direction[1]

        # Check if the next position is out of bounds or blocked
        if not (0 <= next_x < self.n_rows and 0 <= next_y < self.n_cols):
            return False
        if (next_x, next_y) in walls_coord_set or (char_x,char_y) in walls_coord_set:
            return False

        # Valid pull
        return True

    def preprocess(self):
        self.true_costs = []
        all_visited = set(self.walls_coord_set)
        all_squares = set()
        for i in range(len(self.target)):
            visited = set()
            true_cost = [[100000 for _ in range(self.n_cols)] for __ in range(self.n_rows)]
            q = deque()
            q.append((self.target[i],0))
            while q:
                stone_coord , cost = q.popleft()
                if stone_coord in visited:
                    continue
                visited.add(stone_coord)
                true_cost[stone_coord[0]][stone_coord[1]] = cost
                for dir in range(4):
                    if self.can_pull(dir,stone_coord,self.walls_coord_set):
                        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)][dir]
                        stone_x, stone_y = stone_coord[0], stone_coord[1]
                        char_x, char_y = stone_x + direction[0], stone_y + direction[1]
                        new_stone_coord = (char_x,char_y)
                        q.append((new_stone_coord,cost+1))
            self.true_costs.append(true_cost)
            all_visited = all_visited.union(visited)
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                all_squares.add((i,j))
        self.simple_deadlock = all_squares.difference(all_visited)
        #print(sorted(list(self.simple_deadlock)))



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

    def heuristic(self,char_coord, stone_coords, target_coords):
        # Deadlock detection: Check for stones in dead-end corners with no targets
        for stone in stone_coords:
            if self.is_in_deadlock(stone):
                return float('inf')  # Unsolvable state

        n = len(stone_coords)
        cost_matrix = np.zeros((n,n))
        for i,stone in enumerate(stone_coords):
            stone_x,stone_y,w = stone
            for j in range(len(target_coords)):
                cost = self.true_costs[j][stone_x][stone_y]*w
                cost_matrix[i][j] = cost
        row_ind,col_ind = scipy.optimize.linear_sum_assignment(cost_matrix)
        return cost_matrix[row_ind,col_ind].sum()
        '''
        total_distance = 0
        for i, stone in enumerate(stone_coords):
            stone_x, stone_y, w = stone
            min_cost = 10000000
            for j in range(len(self.target)):
                cost = self.true_costs[j][stone_x][stone_y] * w
                min_cost = min(cost,min_cost)
            total_distance+=min_cost
        return total_distance
        '''



    @staticmethod
    def manhattan_distance(coord1, coord2):
        return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

    def is_in_deadlock(self,stone):
        # Extract the x, y coordinates of the stone
        x, y= stone[0], stone[1]
        return (x,y) in self.simple_deadlock

    def A_star(self,time_taken,node_count_shared,path_shared,stop_signal):
        process = psutil.Process()
        start_time = time.time()

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

        # Each state: (f(n),g(n),h(n),current char_coord, list of (stone_x,stone_y,weight), action path)
        start_heuristic = self.heuristic(char_coord,stones_weight_and_coord,self.target)
        q.put((start_heuristic,0,start_heuristic,char_coord, stones_weight_and_coord, ""))
        while q.qsize()>0:
            f_n,g_n,h_n,curr_char_coord, curr_stones_weight_and_coord, path = q.get()
            #extract the stone coord list only
            curr_stones_coord = [(wc[0],wc[1]) for wc in curr_stones_weight_and_coord]
            # Check if all stones are on the switches

            if sorted(curr_stones_coord) == self.target:
                node_count_shared.value = node_count
                path_shared.value = path.encode()
                time_taken.value = time.time() - start_time
                memory = process.memory_info().peak_wset / (1024 * 1024)
                return (path, node_count, time_taken.value, memory)

            if (curr_char_coord, tuple(curr_stones_weight_and_coord)) in visited:
                continue
            #print(node_count)
            node_count += 1
            if node_count % 100 == 0:
                node_count_shared.value = node_count
                time_taken.value = time.time() - start_time
                if stop_signal.is_set():
                    break
            visited.add((curr_char_coord, tuple(curr_stones_weight_and_coord)))
            # Try all 4 possible directions: Up, Down, Left, Right
            for direction in range(4):
                if self.is_move_or_push(direction, curr_char_coord, curr_stones_coord):
                    # Move action
                    if self.can_move(direction, curr_char_coord, self.walls_coord_set):
                        new_char_coord = (curr_char_coord[0] + [-1, 1, 0, 0][direction],
                                          curr_char_coord[1] + [0, 0, -1, 1][direction])
                        #print(f'Curr:{curr_stones_weight_and_coord}')
                        #new_heuristic = self.heuristic(new_char_coord,curr_stones_coord,self.target)
                        new_heuristic =h_n
                        q.put((g_n+1 + new_heuristic,
                               g_n+1,new_heuristic,new_char_coord, curr_stones_weight_and_coord, path + "udlr"[direction]))
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
                            if  (wc[0],wc[1]) == new_char_coord:
                                idx = i
                                break
                        if idx == -1:
                            raise RuntimeError()
                        weight = curr_stones_weight_and_coord[idx][2]
                        new_stones_weight_and_coord[idx] = (new_stone_pos_x, new_stone_pos_y, weight)
                        #print(f'New:{new_stones_weight_and_coord}')
                        new_heuristic = self.heuristic(new_char_coord,new_stones_weight_and_coord,self.target)
                        if new_heuristic == float('inf'):
                            continue
                        q.put((g_n+1+weight+ new_heuristic,
                               g_n+1+weight,new_heuristic,new_char_coord,
                               new_stones_weight_and_coord, path + "UDLR"[direction]))
                        #visited.add((new_char_coord, tuple(new_stones_coord)))
        node_count_shared.value = node_count
        path_shared.value = "No solution found".encode()
        time_taken.value = time.time() - start_time
        memory = process.memory_info().peak_wset / (1024 * 1024)
        return ("No solution found", node_count, time_taken.value, memory)  # If no solution is found
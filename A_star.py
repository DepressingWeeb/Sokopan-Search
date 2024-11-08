import time
from collections import deque
from queue import PriorityQueue
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

    def heuristic(self,char_coord, stone_coords, target_coords):
        # Compute the heuristic as the sum of minimum distances between stones and targets
        total_distance = 0
        # Deadlock detection: Check for stones in dead-end corners with no targets
        for stone in stone_coords:
            if self.is_in_deadlock(stone, target_coords,self.walls_coord_set):
                return float('inf')  # Unsolvable state
        # 1. Calculate the stone-target distance (sum of minimum Manhattan distances)
        stone_sorted = sorted(stone_coords,key= lambda x:-x[2])
        used_target = [False for _ in range(len(target_coords))]

        min_idx = -1
        for stone in stone_sorted:
            min_dist = 1000000
            for i in range(len(target_coords)):
                if used_target[i] :
                    continue
                dist = self.manhattan_distance(stone,target_coords[i])
                if dist<min_dist:
                    min_dist = dist
                    min_idx = i
            total_distance += min_dist * stone[2]
            used_target[min_idx] = True
        # 2. Add the distance from the player to the closest stone (minimizing movement effort)
        #player_to_stone_dist = min(self.manhattan_distance(char_coord, stone) for stone in stone_coords)
        #total_distance += player_to_stone_dist
        return total_distance


    @staticmethod
    def manhattan_distance(coord1, coord2):
        return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

    @staticmethod
    def is_in_deadlock(stone, target_coords, walls_coord_set):
        # Extract the x, y coordinates of the stone
        x, y= stone[0], stone[1]

        # Corner deadlock checks (4 corners)
        if ((x - 1, y) in walls_coord_set and (x, y - 1) in walls_coord_set):
            return (x,y) not in target_coords
        if ((x - 1, y) in walls_coord_set and (x, y + 1) in walls_coord_set):
            return (x,y) not in target_coords
        if ((x + 1, y) in walls_coord_set and (x, y - 1) in walls_coord_set):
            return (x,y) not in target_coords
        if ((x + 1, y) in walls_coord_set and (x, y + 1) in walls_coord_set):
            return (x,y) not in target_coords
        return False


    def A_star(self,time_taken,node_count_shared,path_shared,stop_signal):
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
                return (path,node_count)  # Return the action path

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
        return ("No solution found",node_count)  # If no solution is found
from collections import deque
class DFS:
    def __init__(self, board):
        self.board_begin = board
        self.board = board
        self.n_rows = len(board)
        self.n_cols = len(board[0])
        self.walls_coord_set = set()
        self.target = []
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if board[i][j] == '.':
                    self.target.append((i, j))
                elif board[i][j] == '#':
                    self.walls_coord_set.add((i, j))
        self.target.sort()

    def can_push(self, push_dir, char_coord, stones_coord, walls_coord_set):
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)][push_dir]
        char_x, char_y = char_coord
        stone_x, stone_y = char_x + direction[0], char_y + direction[1]
        next_x, next_y = stone_x + direction[0], stone_y + direction[1]

        if (stone_x, stone_y) not in stones_coord:
            return False
        if not (0 <= next_x < self.n_rows and 0 <= next_y < self.n_cols):
            return False
        if (next_x, next_y) in walls_coord_set or (next_x, next_y) in stones_coord:
            return False
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
    @staticmethod
    def is_in_deadlock(stone, target_coords, walls_coord_set):
        # Extract the x, y coordinates of the stone
        x, y = stone[0], stone[1]
        # Corner deadlock checks (4 corners)
        if ((x - 1, y) in walls_coord_set and (x, y - 1) in walls_coord_set):
            return (x, y) not in target_coords
        if ((x - 1, y) in walls_coord_set and (x, y + 1) in walls_coord_set):
            return (x, y) not in target_coords
        if ((x + 1, y) in walls_coord_set and (x, y - 1) in walls_coord_set):
            return (x, y) not in target_coords
        if ((x + 1, y) in walls_coord_set and (x, y + 1) in walls_coord_set):
            return (x, y) not in target_coords
        return False

    def DFS(self):
        visited = set()
        char_coord = (0, 0)
        stones_coord = []
        node_count = 0

        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if self.board[i][j] == '$':
                    stones_coord.append((i, j))
                elif self.board[i][j] == '@':
                    char_coord = (i, j)

        # Start recursive DFS
        result, path = self._dfs_recursive(char_coord, stones_coord, "", visited, node_count)
        return (path, result)

    def _dfs_recursive(self, char_coord, stones_coord, path, visited, node_count):
        # Check if all stones are on the switches
        if sorted(stones_coord) == self.target:
            return node_count, path
        print(path)
        # Mark the current state as visited
        state = (char_coord, tuple(stones_coord))
        if state in visited:
            return node_count, "No solution found"

        node_count += 1
        visited.add(state)
        for stone in stones_coord:
            if self.is_in_deadlock(stone, self.target ,self.walls_coord_set):
                return node_count, "No solution found"

        for direction in range(4):
            if not self.is_move_or_push(direction, char_coord, stones_coord):
                # Push action
                if self.can_push(direction, char_coord, stones_coord, self.walls_coord_set):
                    # Perform the push
                    new_char_coord = (char_coord[0] + [-1, 1, 0, 0][direction],
                                      char_coord[1] + [0, 0, -1, 1][direction])
                    new_stones_coord = list(stones_coord)
                    new_stone_pos = (new_char_coord[0] + [-1, 1, 0, 0][direction],
                                     new_char_coord[1] + [0, 0, -1, 1][direction])
                    new_stones_coord.remove((new_char_coord[0], new_char_coord[1]))
                    new_stones_coord.append(new_stone_pos)
                    result, new_path = self._dfs_recursive(new_char_coord, new_stones_coord,
                                                           path + "UDLR"[direction], visited, node_count)
                    if new_path != "No solution found":
                        return result, new_path
            else:
                if self.can_move(direction, char_coord, self.walls_coord_set):
                    new_char_coord = (char_coord[0] + [-1, 1, 0, 0][direction],
                                      char_coord[1] + [0, 0, -1, 1][direction])
                    result, new_path = self._dfs_recursive(new_char_coord, stones_coord, path + "udlr"[direction],
                                                           visited, node_count)
                    if new_path != "No solution found":
                        return result, new_path


        # No solution found in this path, return back to previous state
        visited.remove(state)
        return node_count, "No solution found"

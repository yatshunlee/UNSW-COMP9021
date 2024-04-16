from pprint import pprint


class MazeError(Exception):
    pass


class MazeSolver:
    def __init__(self, maze, start, *, target_val=0, endpoints=None):
        self.to_visit = [start]
        self.visited = set()
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.endpoints = endpoints
        self.maze = maze
        self.m = len(maze)
        self.n = len(maze[0])

    def traverse(self):
        pass


class Maze:
    def __init__(self, fname):
        self.fname = fname
        file = open(self.fname)
        lines = file.read().split('\n')

        self.edges = []
        for sentence in lines:
            row = []
            for char in sentence:
                # contains not 0-3 nor space
                if char in ['0', '1', '2', '3']:
                    row.append(char)
                elif char != ' ':
                    raise MazeError('Incorrect input')  # contains not only {0, 1, 2, 3, space}
            # store nonempty row / line
            if len(row):
                self.edges.append(row)
        del lines

        for i in range(len(self.edges)):
            if i != 0 and len(self.edges[i]) != len(self.edges[0]):
                raise MazeError('Incorrect input')  # inconsistency
            if self.edges[i][-1] in ['1', '3']:
                raise MazeError("Input does not represent a maze.")  # >=1 lines contains 1 or 3 at last digit
        if '2' in self.edges[-1] or '3' in self.edges[-1]:
            raise MazeError("Input does not represent a maze.")  # >=1 lines contains 2 or 3 at last row
        if len(self.edges) < 2 or len(self.edges) > 41:
            raise MazeError('Incorrect input')  # too few or many nonblank lines
        if len(self.edges[0]) < 2 or len(self.edges[0]) > 31:
            raise MazeError('Incorrect input')  # too few or many nonblank digits on a line

        # create maze
        self.create_maze()

    def create_maze(self):
        self.maze = []
        for i in range(2 * len(self.edges) - 1):
            row = []
            for j in range(2 * len(self.edges[0]) - 1):
                row.append(0)
            self.maze.append(row)

        for i in range(0, len(self.edges) - 1):
            for j in range(len(self.edges[0]) - 1):
                if self.edges[i][j] == '1':
                    a, b, c = 1, 1, 1
                    d, e, f = 0, 0, 0
                    x, y, z = 0, 0, 0
                elif self.edges[i][j] == '2':
                    a, b, c = 1, 0, 0
                    d, e, f = 1, 0, 0
                    x, y, z = 1, 0, 0
                elif self.edges[i][j] == '3':
                    a, b, c = 1, 1, 1
                    d, e, f = 1, 0, 0
                    x, y, z = 1, 0, 0
                else:
                    a, b, c = 0, 0, 0
                    d, e, f = 0, 0, 0
                    x, y, z = 0, 0, 0

                self.maze[i * 2 + 0][j * 2 + 0] = max(self.maze[i * 2 + 0][j * 2 + 0], a)
                self.maze[i * 2 + 0][j * 2 + 1] = max(self.maze[i * 2 + 0][j * 2 + 1], b)
                self.maze[i * 2 + 0][j * 2 + 2] = max(self.maze[i * 2 + 0][j * 2 + 2], c)
                self.maze[i * 2 + 1][j * 2 + 0] = max(self.maze[i * 2 + 1][j * 2 + 0], d)
                self.maze[i * 2 + 1][j * 2 + 1] = max(self.maze[i * 2 + 1][j * 2 + 1], e)
                self.maze[i * 2 + 1][j * 2 + 2] = max(self.maze[i * 2 + 1][j * 2 + 2], f)
                self.maze[i * 2 + 2][j * 2 + 0] = max(self.maze[i * 2 + 2][j * 2 + 0], x)
                self.maze[i * 2 + 2][j * 2 + 1] = max(self.maze[i * 2 + 2][j * 2 + 1], y)
                self.maze[i * 2 + 2][j * 2 + 2] = max(self.maze[i * 2 + 2][j * 2 + 2], z)

        for i in range(len(self.edges) - 1):
            if self.edges[i][-1] == '2':
                a, b, c = 1, 1, 1
            else:
                a, b, c = 0, 0, 0
            self.maze[i * 2 + 0][-1] = max(self.maze[i * 2 + 0][-1], a)
            self.maze[i * 2 + 1][-1] = max(self.maze[i * 2 + 1][-1], b)
            self.maze[i * 2 + 2][-1] = max(self.maze[i * 2 + 2][-1], c)
        for j in range(len(self.edges[0]) - 1):
            if self.edges[-1][j] == '1':
                a, b, c = 1, 1, 1
            else:
                a, b, c = 0, 0, 0
            self.maze[-1][j * 2 + 0] = max(self.maze[-1][j * 2 + 0], a)
            self.maze[-1][j * 2 + 1] = max(self.maze[-1][j * 2 + 1], b)
            self.maze[-1][j * 2 + 2] = max(self.maze[-1][j * 2 + 2], c)

        self.maze_map = []
        for i in range(len(self.maze)):
            row = []
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == 1:
                    row.append('w')
                elif i % 2 == 0 or j % 2 == 0:
                    row.append(' ')
                else:
                    row.append('n')
            self.maze_map.append(row)

    def analyse(self):
        ########### gate counting ###########
        all_gates = []
        # check left and right edges
        for i in range(1, len(self.maze), 2):
            if self.maze[i][0] == 0:
                all_gates.append((i, 0))
            if self.maze[i][-1] == 0:
                all_gates.append((i, len(self.maze[0]) - 1))
        # check top and bottom edges
        for j in range(1, len(self.maze[0]), 2):
            if self.maze[0][j] == 0:
                all_gates.append((0, j))
            if self.maze[-1][j] == 0:
                all_gates.append((len(self.maze) - 1, j))

        gate_cnt = len(all_gates)
        if gate_cnt > 1:
            print('The maze has', gate_cnt, 'gates.')
        elif gate_cnt == 1:
            print('The maze has a single gate.')
        else:
            print('The maze has no gate.')

        ########### find pillars ############
        self.pillars = []
        for i in range(0, len(self.maze_map), 2):
            for j in range(0, len(self.maze_map[0]), 2):
                if self.maze_map[i][j] != ' ':
                    continue
                cnt = 0
                if i > 0 and j > 0:
                    cnt += self.maze_map[i - 1][j - 1] == 'n'
                if i < len(self.maze_map) - 1 and j > 0:
                    cnt += self.maze_map[i + 1][j - 1] == 'n'
                if i > 0 and j < len(self.maze_map[0]) - 1:
                    cnt += self.maze_map[i - 1][j + 1] == 'n'
                if i < len(self.maze_map) - 1 and j < len(self.maze_map[0]) - 1:
                    cnt += self.maze_map[i + 1][j + 1] == 'n'
                if cnt == 4:
                    self.pillars.append((i, j))
                else:
                    cond = (i == 0 or i == len(self.maze_map) - 1) + (j == 0 or j == len(self.maze_map[0]) - 1)
                    if cond and cnt == 2:
                        self.pillars.append((i, j))
                    elif cond == 2 and cnt == 1:
                        self.pillars.append((i, j))

        ########### traverse the maze ###########
        node_gate_mapping = {}
        gate_node_mapping = {}
        for i, j in all_gates:
            if i % 2 == 0:
                if i == 0:
                    node = (i + 1, j)
                else:
                    node = (i - 1, j)
            else:
                if j == 0:
                    node = (i, j + 1)
                else:
                    node = (i, j - 1)
            node_gate_mapping.setdefault(node, [])
            node_gate_mapping[node].append((i, j))
            gate_node_mapping[(i, j)] = node

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        visited = set()
        gate_gate_mapping = {}  # (start, end): nodes in between
        gate_cds_mapping = {}

        gate_other_gates_mapping = {}
        accessible_areas_cnt = 0
        intersections = set()
        for start in all_gates:
            node = gate_node_mapping[start]
            if node in visited:
                continue
            to_visit = [node]
            visited.add(node)
            paths = [[node]]
            accessible_areas_cnt += 1
            while len(to_visit):
                i, j = to_visit.pop(0)
                path = paths.pop(0)

                wall_cnt = 0
                intersection_cnt = 0
                for di, dj in directions:
                    if i + di == 0 or i + di == len(self.maze) - 1 or j + dj == 0 or j + dj == len(self.maze[0]) - 1:
                        if gate_node_mapping.get((i + di, j + dj)):  # if is gate
                            intersection_cnt += 1
                            end = (i + di, j + dj)
                            if start == end:
                                continue
                            gate_gate_mapping[(start, end)] = path
                            gate_other_gates_mapping.setdefault(start, set())
                            gate_other_gates_mapping[start].add(end)

                        else:  # then is a wall
                            wall_cnt += 1

                    elif self.maze[i + di][j + dj] == 0:
                        intersection_cnt += 1
                        # if visited >> no go
                        if (i + di * 2, j + dj * 2) in visited:
                            continue
                        # if not visited and no wall >> go
                        to_visit.append((i + di * 2, j + dj * 2))
                        visited.add((i + di * 2, j + dj * 2))
                        # store the new node to the new path
                        new_path = path[:]
                        new_path.append((i + di * 2, j + dj * 2))
                        paths.append(new_path)

                    else:
                        wall_cnt += 1

                # all cul-de-sacs have 3 walls
                if wall_cnt == 3:
                    end = (i, j)
                    gate_cds_mapping[(start, end)] = path
                # if more than 1 path that you can go
                elif intersection_cnt > 2:
                    intersections.add((i, j))

        wall_nodes = []
        all_non_wall_nodes = set()
        for i in range(len(self.maze_map)):
            for j in range(len(self.maze_map[0])):
                if self.maze_map[i][j] == 'w':
                    wall_nodes.append((i, j))
                elif self.maze_map[i][j] == 'n':
                    all_non_wall_nodes.add((i, j))
        wall_visited = set()
        wall_cnt = 0
        for wn in wall_nodes:
            if wn in wall_visited:
                continue
            wall_visited.add(wn)
            to_visit_wall = [wn]
            while len(to_visit_wall) > 0:
                i, j = to_visit_wall.pop()
                for di, dj in directions:
                    if i + di < 0 or i + di >= len(self.maze_map):
                        continue
                    if j + dj < 0 or j + dj >= len(self.maze_map[0]):
                        continue
                    if (i + di, j + dj) in wall_visited:
                        continue
                    if self.maze_map[i + di][j + dj] == 'w':
                        to_visit_wall.append((i + di, j + dj))
                        wall_visited.add((i + di, j + dj))
            wall_cnt += 1

        # BFS result
        shortest_path_nodes = set()
        for gg in gate_gate_mapping:
            shortest_path_nodes = shortest_path_nodes.union(set(gate_gate_mapping[gg]))

        gates = set()
        cds = set()
        for gc in gate_cds_mapping:
            gates.add(gc[0])
            cds.add(gc[1])
            shortest_path_nodes = shortest_path_nodes.union(set(gate_cds_mapping[gc]))

        # inaccessible nodes
        inaccessible_nodes = all_non_wall_nodes.difference(visited)

        # accessible nodes but you did not walk
        excess_nodes = all_non_wall_nodes.intersection(visited).difference(shortest_path_nodes)

        ########### sets of connected walls counting ###########
        if wall_cnt > 1:
            print('The maze has', wall_cnt, 'sets of walls that are all connected.')
        elif wall_cnt == 1:
            print('The maze has walls that are all connected.')
        else:
            print('The maze has no wall.')

        ########### inaccessible inner points counting ###########
        inaccessible_area_cnt = len(inaccessible_nodes)
        if inaccessible_area_cnt > 1:
            print('The maze has', inaccessible_area_cnt, 'inaccessible inner points.')
        elif inaccessible_area_cnt == 1:
            print('The maze has a unique inaccessible inner point.')
        else:
            print('The maze has no inaccessible inner point.')

        ########### accessible areas counting ###########
        if accessible_areas_cnt > 1:
            print('The maze has', accessible_areas_cnt, 'accessible areas.')
        elif accessible_areas_cnt == 1:
            print('The maze has a unique accessible area.')
        else:
            print('The maze has no accessible area.')

        ########### accessible cul-de-sacs counting ###########
        cul_de_sacs_cnt = 0
        cul_de_sacs = []
        for gc in gate_cds_mapping:
            start, end = gc
            cul_de_sacs.append(end)
            for interstep in gate_cds_mapping[gc][::-1]:
                existing_intersection_cnt = 0
                if interstep not in intersections:
                    cul_de_sacs.append(interstep)
                    continue
                else:
                    i, j = interstep
                    for di, dj in directions:
                        # if near gate
                        if i + di == 0 or i + di == len(self.maze) - 1 or j + dj == 0 or j + dj == len(self.maze[0]) - 1:
                            is_gate = gate_node_mapping.get((i + di, j + dj))
                            if is_gate:
                                existing_intersection_cnt += 1
                        elif self.maze[i + di][j + dj] == 0:
                            if (i + di * 2, j + dj * 2) in cul_de_sacs:
                                continue
                            existing_intersection_cnt += 1

                    if existing_intersection_cnt == 1:
                        cul_de_sacs.append(interstep)
                    else:
                        break

        cul_de_sacs = set(cul_de_sacs)
        for i, j in cul_de_sacs:
            self.maze_map[i][j] = 'x'

        cul_de_sacs_entrances = set()
        cul_de_sacs_visited = set()
        for gc in gate_cds_mapping:
            start, _ = gc
            node = gate_node_mapping[start]
            if node in cul_de_sacs_visited:
                continue
            cul_de_sacs_visited.add(node)
            i, j = node
            if self.maze_map[i][j] == 'x':
                cul_de_sacs_entrances.add((i, j))
                continue
            cul_de_sacs_to_visit = [node]
            while len(cul_de_sacs_to_visit):
                i, j = cul_de_sacs_to_visit.pop()
                for di, dj in directions:
                    if i + di == 0 or i + di == len(self.maze) - 1 or j + dj == 0 or j + dj == len(self.maze[0]) - 1:
                        continue

                    elif self.maze[i + di][j + dj] == 0:
                        if (i + di * 2, j + dj * 2) in cul_de_sacs_visited:
                            continue
                        if self.maze_map[i + di * 2][j + dj * 2] == 'x':
                            cul_de_sacs_entrances.add((i + di * 2, j + dj * 2))
                        else:
                            cul_de_sacs_to_visit.append((i + di * 2, j + dj * 2))
                        cul_de_sacs_visited.add((i + di * 2, j + dj * 2))


        cul_de_sacs_cnt = len(cul_de_sacs_entrances)
        if cul_de_sacs_cnt > 1:
            print('The maze has', cul_de_sacs_cnt, 'accessible cul-de-sacs that are all connected.')
        elif cul_de_sacs_cnt == 1:
            print('The maze has accessible cul-de-sacs that are all connected.')
        else:
            print('The maze has no accessible cul-de-sac.')

        ########### entry exit path counting ###########
        excess_nodes_visited = set()
        non_unique_gates_groups = {}
        for node in excess_nodes:
            if node in excess_nodes_visited:
                continue
            excess_nodes_visited.add(node)
            to_visit_excess_nodes = [node]
            non_unique_gates_groups[node] = []
            while len(to_visit_excess_nodes):
                i, j = to_visit_excess_nodes.pop()
                for di, dj in directions:
                    if i + di == 0 or i + di == len(self.maze) - 1 or j + dj == 0 or j + dj == len(self.maze[0]) - 1:
                        is_gate = gate_node_mapping.get((i + di, j + dj))
                        if is_gate:  # if is gate
                            non_unique_gates_groups[node].append((i + di, j + dj))

                    elif self.maze[i + di][j + dj] == 0:
                        # if visited >> no go
                        if (i + di * 2, j + dj * 2) in excess_nodes_visited:
                            continue
                        # if not visited and no wall >> go
                        to_visit_excess_nodes.append((i + di * 2, j + dj * 2))
                        excess_nodes_visited.add((i + di * 2, j + dj * 2))

        self.unique_gate_pairs = []
        for start in gate_other_gates_mapping:
            if len(gate_other_gates_mapping[start]) == 1:
                end = list(gate_other_gates_mapping[start])[0]
                is_unique = True
                for non_unique_group in non_unique_gates_groups.values():
                    if start in non_unique_group and end in non_unique_group:
                        is_unique = False
                        break
                if is_unique:
                    path = [start] + gate_gate_mapping[(start, end)] + [end]
                    self.unique_gate_pairs.append(path)

        entry_exit_path_cnt = len(self.unique_gate_pairs)
        if entry_exit_path_cnt > 1:
            print('The maze has', entry_exit_path_cnt, 'entry-exit paths with no intersections not to cul-de-sacs.')
        elif entry_exit_path_cnt == 1:
            print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')

    def display(self):
        # for row in self.maze_map:
        #     print('  ', *row)

        output = ['\\documentclass[10pt]{article}',
                  '\\usepackage{tikz}',
                  '\\usetikzlibrary{shapes.misc}',
                  '\\usepackage[margin=0cm]{geometry}',
                  '\\pagestyle{empty}',
                  '\\tikzstyle{every node}=[cross out, draw, red]',
                  '',
                  '\\begin{document}',
                  '',
                  '\\vspace*{\\fill}',
                  '\\begin{center}',
                  '\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]']
        output.append('% Walls')
        for i in range(0, len(self.maze_map), 2):
            for j in range(0, len(self.maze_map[0]), 2):
                if self.maze_map[i][j] != 'w':
                    continue
                if i != len(self.maze_map) - 1:
                    if self.maze_map[i + 1][j] == 'w':
                        s = f"    \\draw ({j // 2},{i // 2}) -- ({j // 2},{i // 2 + 1});"
                        output.append(s)
                if j != len(self.maze_map[0]) - 1:
                    if self.maze_map[i][j + 1] == 'w':
                        s = f"    \\draw ({j // 2},{i // 2}) -- ({j // 2 + 1},{i // 2});"
                        output.append(s)
        output.append('% Pillars')
        for i, j in self.pillars:
            s = f"    \\fill[green] ({j // 2},{i // 2}) circle(0.2);"
            output.append(s)
        output.append('% Inner points in accessible cul-de-sacs')
        for i in range(len(self.maze_map)):
            for j in range(len(self.maze_map[0])):
                if self.maze_map[i][j] == 'x':
                    s = f"    \\node at ({j / 2},{i / 2})" + " {};"
                    output.append(s)
        output.append('% Entry-exit paths without intersections')
        for path in self.unique_gate_pairs:
            for i in range(len(path) - 1):
                prev = path[i]
                nxt = path[i + 1]
                s = f"    \\draw[dashed, yellow] ({prev[1] / 2},{prev[0] / 2}) -- ({nxt[1] / 2},{nxt[0] / 2});"
                output.append(s)
        ending = [
            "",
            "\\end{tikzpicture}",
            "\\end{center}",
            "\\vspace*{\\fill}",
            "\\end{document}"]
        output.extend(ending)
        with open(f'{self.fname[:-4]}.tex', 'w') as file:
            file.write('\n'.join(output))
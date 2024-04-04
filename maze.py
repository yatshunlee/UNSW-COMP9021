class MazeError(Exception):
    pass

    
class Maze:
    def __init__(self, f):
        f = open(f)
        lines = f.read().split('\n')

        self.edges = []
        for sentence in lines:
            row = []
            for char in sentence:
                # contains not 0-3 nor space
                if char in ['0', '1', '2', '3']:
                    row.append(char)
                elif char != ' ':
                    raise MazeError('Incorrect input') # contains not only {0, 1, 2, 3, space}
            # store nonempty row / line
            if len(row):
                self.edges.append(row)
        del lines

        for i in range(len(self.edges)):
            if i != 0 and len(self.edges[i]) != len(self.edges[0]):
                raise MazeError('Incorrect input') # inconsistency
            if self.edges[i][-1] in ['1', '3']:
                raise MazeError("Input does not represent a maze.") # >=1 lines contains 1 or 3 at last digit
        if '2' in self.edges[-1] or '3' in self.edges[-1]:
            raise MazeError("Input does not represent a maze.") # >=1 lines contains 2 or 3 at last row
        if len(self.edges) < 2 or len(self.edges) > 41:
            raise MazeError('Incorrect input')  # too few or many nonblank lines
        if len(self.edges[0]) < 2 or len(self.edges[0]) > 31:
            raise MazeError('Incorrect input')  # too few or many nonblank digits on a line
    
    def analyze(self):
        # gate counting
        gate_cnt = 0
        # horizontal
        for j in range(len(self.edges[0]) - 1):
            # top
            if self.edges[0][j] in ['0', '2']:
                gate_cnt += 1
            # bottom
            if self.edges[-1][j] in ['0', '2']:
                gate_cnt += 1
        # vertical
        for i in range(len(self.edges) - 1):
            if self.edges[i][0] in ['0', '1']:
                gate_cnt += 1
            if self.edges[i][-1] in ['0', '1']:
                gate_cnt += 1

        if gate_cnt > 1:
            print('The maze has', gate_cnt, 'gates.')
        elif gate_cnt == 1:
            print('The maze has a single gate.')
        else:
            print('The maze has no gate.')

        if gate_cnt > 1:
            print('The maze has', gate_cnt, 'sets of walls that are all connected.')
        elif gate_cnt == 1:
            print('The maze has walls that are all connected.')
        else:
            print('The maze has no wall.')

        if gate_cnt > 1:
            print('The maze has', gate_cnt, 'inaccessible inner points.')
        elif gate_cnt == 1:
            print('The maze has a unique inaccessible inner point.')
        else:
            print('The maze has no inaccessible inner point.')

        if gate_cnt > 1:
            print('The maze has', gate_cnt, 'accessible areas.')
        elif gate_cnt == 1:
            print('The maze has a unique accessible area.')
        else:
            print('The maze has no accessible area.')

        if gate_cnt > 1:
            print('The maze has', gate_cnt, 'accessible cul-de-sacs that are all connected.')
        elif gate_cnt == 1:
            print('The maze has accessible cul-de-sacs that are all connected.')
        else:
            print('The maze has no accessible cul-de-sac.')

        if gate_cnt > 1:
            print('The maze has', gate_cnt, 'entry-exit paths with no intersections not to cul-de-sacs.')
        elif gate_cnt == 1:
            print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')

    def display(self):
        print(self.edges)
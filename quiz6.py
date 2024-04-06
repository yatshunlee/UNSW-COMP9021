# Quiz 6 *** Due Thursday Week 9 @ 9.00pm
# Randomly generates a grid of 0s and 1s and determines
# the maximum number of "spikes" in a shape.
# A shape is made up of 1s connected horizontally or vertically (it can contain holes).
# A "spike" in a shape is a 1 that is part of this shape and "sticks out"
# (has exactly one neighbour in the shape).
# Neighbours are only considered vertically or horizontally (not diagonally).
# Note that a shape with a single 1 is also a spike.

from random import seed, randrange
import sys


dim = 10


def display_grid():
    for row in grid:
        print('   ', *row) 


# Returns the number of shapes we have discovered and "coloured".
# We "colour" the first shape we find by replacing all the 1s
# that make it with 2. We "colour" the second shape we find by
# replacing all the 1s that make it with 3.
def colour_shapes():
    """use of dictionary"""
    all_nodes = [(i, j) for i in range(dim) for j in range(dim) if i != 0 or j != 0]
    visited = {}
    color = 1
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while len(all_nodes) > 0:
        new = all_nodes.pop(0)
        visited = set()
        to_visit = [new]
        first = True

        while len(to_visit) > 0:
            i, j = to_visit.pop(0)
            if (i, j) in visited:
                continue
            visited.add((i, j))
            if grid[i][j] != 1:
                continue
            if first:
                first = False
                color += 1
            grid[i][j] = color
            for di, dj in directions:
                # out of grid
                if i + di >= dim or i + di < 0:
                    continue
                if j + dj >= dim or j + dj < 0:
                    continue
                if grid[i + di][j + dj] == 1:
                    if (i + di, j + dj) in visited:
                        continue
                    to_visit.append((i + di, j + dj))

    return color - 1


def max_number_of_spikes(nb_of_shapes):
    """count spike"""
    res = {}
    for v in range(nb_of_shapes):
        v += 2
        res[v] = 0
        for i in range(dim):
            for j in range(dim):
                if grid[i][j] != v:
                    continue
                res[v] += is_spike(i, j, v)
    return max(res.values())
    # Replace pass above with your code

# Possibly define other functions here
def is_spike(i, j, v):
    """
    determine if a cell is a spike
    :return: True if no neighbor in the grid is 1.
    """
    # vector of up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    cnt = 0
    for di, dj in directions:
        # out of grid
        if i + di >= dim or i + di < 0:
            continue
        if j + dj >= dim or j + dj < 0:
            continue
        if grid[i+di][j+dj] == v:
            if cnt == 1:
                return 0
            cnt += 1
    return 1

try: 
    for_seed, density = (int(x) for x in input('Enter two integers, the second '
                                               'one being strictly positive: '
                                              ).split()
                    )
    if density <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[int(randrange(density) != 0) for _ in range(dim)]
            for _ in range(dim)
       ]
print('Here is the grid that has been generated:')
display_grid()
nb_of_shapes = colour_shapes()
print('The maximum number of spikes of some shape is:',
      max_number_of_spikes(nb_of_shapes)
     )
from random import seed, randrange
import sys


dim = 10

def display_grid(grid):
    for row in grid:
        print('   ', *row)

"""
Intuition

############ 11
#########     8
####          3
##########    9

i, j = 0, 0

max_j = 11
max_i =  3
min([11, 8, 3, 9]) = 3
argmin([11, 8, 3, 9]) = 2

(3+1) * (2+1) = 12
"""

def get_left_shift_grid():
    left_grid = []
    for i in range(dim):
        left_grid.append([0]*(dim-i-1) + grid[i] + [0]*i)
    return left_grid

def get_right_shift_grid():
    right_grid = []
    for i in range(dim):
        right_grid.append([0]*i + grid[i] + [0]*(dim-i-1))
    return right_grid

def largest_rectangle(bars):
    st, res = [], 0
    for bar in bars + [-1]: # add -1 to have an additional iteration
        step = 0
        while st and st[-1][1] >= bar:
            w, h = st.pop()
	    step += w
	    res = max(res, step * h)

        st.append((step + 1, bar))

    return res

def size_of_largest_parallelogram(grid):
    max_size = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                continue
            if j == len(grid[0]) - 1:
                continue
            max_w = 1
            while j + max_w < len(grid[0]):
                if grid[i][j+max_w] == 0:
                    break
                max_w += 1
            max_h = 1
            widths = [max_w]
            while i + max_h < len(grid):
                for w in range(max_w):
                    if grid[i+max_h][j+w] == 0:
                        w -= 1
                        break
                if w < 1:
                    break
                widths.append(w+1)
                max_h += 1
            if len(widths) <= 1:
                continue
            size = largest_rectangle(widths)
            # print(max_w, widths)
            # print("Top Left Cell:", (i, j), "with a maximum size of", size)
            max_size = max(max_size, size)
    return max_size

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
display_grid(grid)
lgrid = get_left_shift_grid()
rgrid = get_right_shift_grid()

max_size = 0
for g in [grid, lgrid, rgrid]:
    # display_grid(g)
    size = size_of_largest_parallelogram(g)
    max_size = max(size, max_size)
size = max_size

if size:
    print('The largest parallelogram with horizontal sides '
          f'has a size of {size}.'
         )
else:
    print('There is no parallelogram with horizontal sides.')

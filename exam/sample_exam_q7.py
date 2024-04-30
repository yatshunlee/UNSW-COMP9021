# Sample Exam Question 7

# Write a function that accepts a strictly positive integer called height
# and displays a triangle shape of numbers starting from 0 and of height height.
# Use only digits from 0 to 9 to construct the shape as per the examples below:



'''
Will be tested with height a strictly positive integer.
'''


def f(height):
    '''
    >>> f(1)
    0
    >>> f(2)
     0
    123
    >>> f(3)
      0
     123
    45678
    >>> f(4)
       0
      123
     45678
    9012345
    >>> f(5)
        0
       123
      45678
     9012345
    678901234
    >>> f(6)
         0
        123
       45678
      9012345
     678901234
    56789012345
    >>> f(20)
                       0
                      123
                     45678
                    9012345
                   678901234
                  56789012345
                 6789012345678
                901234567890123
               45678901234567890
              1234567890123456789
             012345678901234567890
            12345678901234567890123
           4567890123456789012345678
          901234567890123456789012345
         67890123456789012345678901234
        5678901234567890123456789012345
       678901234567890123456789012345678
      90123456789012345678901234567890123
     4567890123456789012345678901234567890
    123456789012345678901234567890123456789
    '''
    # Insert your code here
    j = 0
    def width_limit(h):
        return ((h - 1) * 2) + 1

    # tree = [[0], [1,2,3], ...]
    tree = []
    for i in range(height):
        layer = ''
        for k in range(width_limit(i+1)):
            layer += str(j % 10)
            j += 1
        tree.append(layer)

    multipler = 1
    for level in range(height-2, -1, -1):
        tree[level] = ' ' * multipler + tree[level]
        multipler += 1

    print('\n'.join(tree))



if __name__ == '__main__':
    import doctest
    doctest.testmod()
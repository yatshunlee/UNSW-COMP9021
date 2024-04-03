# Sample Exam Question 8

# Write a function that accepts a string of DISTINCT UPPERCASE letters only
# called letters and displays all pairs of words using all (distinct) letters in letters.

# Please note that the words need to be valid. Use the provided dictionary.txt
# to check the validity of words.

'''
Will be tested with letters, a string of DISTINCT UPPERCASE letters only.
'''



def f(letters):
    '''
    >>> f('ABCDEFGH')
    There is no solution
    >>> f('GRIHWSNYP')
    The pairs of words using all (distinct) letters in "GRIHWSNYP" are:
    ('SPRING', 'WHY')
    >>> f('ONESIX')
    The pairs of words using all (distinct) letters in "ONESIX" are:
    ('ION', 'SEX')
    ('ONE', 'SIX')
    >>> f('UTAROFSMN')
    The pairs of words using all (distinct) letters in "UTAROFSMN" are:
    ('AFT', 'MOURNS')
    ('ANT', 'FORUMS')
    ('ANTS', 'FORUM')
    ('ARM', 'FOUNTS')
    ('ARMS', 'FOUNT')
    ('AUNT', 'FORMS')
    ('AUNTS', 'FORM')
    ('AUNTS', 'FROM')
    ('FAN', 'TUMORS')
    ('FANS', 'TUMOR')
    ('FAR', 'MOUNTS')
    ('FARM', 'SNOUT')
    ('FARMS', 'UNTO')
    ('FAST', 'MOURN')
    ('FAT', 'MOURNS')
    ('FATS', 'MOURN')
    ('FAUN', 'STORM')
    ('FAUN', 'STROM')
    ('FAUST', 'MORN')
    ('FAUST', 'NORM')
    ('FOAM', 'TURNS')
    ('FOAMS', 'RUNT')
    ('FOAMS', 'TURN')
    ('FORMAT', 'SUN')
    ('FORUM', 'STAN')
    ('FORUMS', 'NAT')
    ('FORUMS', 'TAN')
    ('FOUNT', 'MARS')
    ('FOUNT', 'RAMS')
    ('FOUNTS', 'RAM')
    ('FUR', 'MATSON')
    ('MASON', 'TURF')
    ('MOANS', 'TURF')
    '''
    dictionary = 'dictionary.txt'
    solutions = []

    # Insert your code here
    with open(dictionary, 'r') as infile:
        words = sorted(infile.read().split('\n'))

    def is_valid_pair(word1, word2, letters):
        word_set = word1 + word2
        return len(word_set) == len(letters) and set(word_set) == set(letters)

    def find_pairs(letters, dictionary):
        valid_pairs = []
        for i in range(len(dictionary)):
            word1 = dictionary[i]
            for j in range(i+1, len(dictionary)):
                word2 = dictionary[j]
                if is_valid_pair(word1, word2, letters):
                    pair = tuple(sorted([word1, word2]))
                    if pair in valid_pairs:
                        continue
                    valid_pairs.append(pair)
        return valid_pairs

    words.sort()
    solutions = find_pairs(letters, words)

    if not solutions:
        print('There is no solution')
    else:
        print(f'The pairs of words using all (distinct) letters in "{letters}" are:')
        for solution in solutions:
            print(solution)


if __name__ == '__main__':
    import doctest

    doctest.testmod()

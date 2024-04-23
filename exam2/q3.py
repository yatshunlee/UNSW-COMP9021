#Question 3

'''
Given a word w, a good subsequence of w is defined as a word w' such that
- all letters in w' are different;
- w' is obtained from w by deleting some letters in w.

Returns the list of all good subsequences, without duplicates, in lexicographic order
(recall that the sorted() function sorts strings in lexicographic order).

The number of good sequences grows exponentially in the number of distinct letters in w,
so the function will be tested only for cases where the latter is not too large.

'''

def good_subsequences(word):
    '''
    >>> good_subsequences('')
    ['']
    >>> good_subsequences('aaa')
    ['', 'a']
    >>> good_subsequences('aaabbb')
    ['', 'a', 'ab', 'b']
    >>> good_subsequences('aaabbc')
    ['', 'a', 'ab', 'abc', 'ac', 'b', 'bc', 'c']
    >>> good_subsequences('aaabbaaa')
    ['', 'a', 'ab', 'b', 'ba']
    >>> good_subsequences('abbbcaaabccc')
    ['', 'a', 'ab', 'abc', 'ac', 'acb', 'b', 'ba', 'bac',\
 'bc', 'bca', 'c', 'ca', 'cab', 'cb']
    >>> good_subsequences('abbbcaaabcccaaa')
    ['', 'a', 'ab', 'abc', 'ac', 'acb', 'b', 'ba', 'bac',\
 'bc', 'bca', 'c', 'ca', 'cab', 'cb', 'cba']
    >>> good_subsequences('abbbcaaabcccaaabbbbbccab')
    ['', 'a', 'ab', 'abc', 'ac', 'acb', 'b', 'ba', 'bac',\
 'bc', 'bca', 'c', 'ca', 'cab', 'cb', 'cba']
    >>> good_subsequences('abcb')
    ['', 'a', 'ab', 'abc', 'ac', 'acb', 'b', 'bc', 'c', 'cb']
    '''
    # Insert your code here
    o = ''
    if len(word) > 0:
        o = word[0]
        for i in range(1, len(word)):
            if o[-1] != word[i]:
              o += word[i]

    output = []
    end_count = len(set(o))
    def dfs(options, path):
        if path not in output: 
            output.append(path[:])
            if len(path) == end_count:
                return
            for i in range(len(options)):
                if options[i] not in path: 
                    new = options[i+1:]
                    path += options[i]
                    dfs(new, path)
                    path = path[:-1]

    dfs(o, '')
    return sorted(output)



# Possibly define another function


if __name__ == '__main__':
    import doctest
    doctest.testmod()
# Sample Exam Question 5

# Write a function that accepts a year between 1913 and 2013 inclusive
# and displays the maximum inflation during that year and the month(s)
# in which it was achieved.
'''
Will be tested with year between 1913 and 2013 .
You might find the reader() function of the csv module useful,
but you can also use the split() method of the str class.
'''

import csv

def f(year):
    '''
    >>> f(1914)
    In 1914, maximum inflation was: 2.0
    It was achieved in the following months: Aug
    >>> f(1922)
    In 1922, maximum inflation was: 0.6
    It was achieved in the following months: Jul, Oct, Nov, Dec
    >>> f(1995)
    In 1995, maximum inflation was: 0.4
    It was achieved in the following months: Jan, Feb
    >>> f(2013)
    In 2013, maximum inflation was: 0.82
    It was achieved in the following months: Feb
    '''
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    # Insert your code here

    # Open the CSV file
    o = []
    with open('cpiai.csv', 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Each row is a list of values representing the columns in that row
            date, _, inflation = row
            if date[:4] == str(year):
                o.append(float(inflation))
        
    output_months = []
    for i in range(len(o)):
        if max(o) == o[i]:
            output_months.append(months[i])
    output_months = ', '.join(output_months)
    print(f'In {year}, maximum inflation was: {max(o)}')
    print(f'It was achieved in the following months: {output_months}')
        
if __name__ == '__main__':
    
    import doctest
    doctest.testmod()
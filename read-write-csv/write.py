import csv

CSV_PATH = './output/test.csv'

DICTS = [
    {
        'name': 'John',
        'age': 43,
        'sex': 'M'
    },
    {
        'name': 'Mary',
        'age': 39,
        'sex': 'F'
    },
    {
        'name': 'Max',
        'age': 17,
        'sex': 'M'
    },
    {
        'name': 'Tiffany',
        'age': 21,
        'sex': 'F'
    }
]

# Alternatively you can use
# keys = DICTS[0].keys() if you are sure your list has values
keys = ['name', 'age', 'sex']

with open(CSV_PATH, 'w') as output_file:
    dict_writter = csv.DictWriter(output_file, DICTS[0].keys())
    dict_writter.writeheader()
    dict_writter.writerows(DICTS)
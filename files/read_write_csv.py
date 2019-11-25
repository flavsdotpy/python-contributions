import csv

# Write from list of dicts
list_of_dicts = [
    {'name': 'John', 'age': 43, 'sex': 'M'},
    {'name': 'Mary', 'age': 39, 'sex': 'F'},
    {'name': 'Max', 'age': 17, 'sex': 'M'},
    {'name': 'Tiffany', 'age': 21, 'sex': 'F'}
]
with open('./output.csv', 'w') as output_file:
    dict_writter = csv.DictWriter(output_file, list_of_dicts[0].keys())
    dict_writter.writeheader()
    dict_writter.writerows(list_of_dicts)

# Read to list of dicts
with open('./resources/input.csv') as f:
    csv_dict = list(csv.DictReader(f))
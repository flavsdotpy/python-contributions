import csv

CSV_PATH = 'input/sample.csv'


with open(CSV_PATH) as f:
    csv_dict = list(csv.DictReader(f))

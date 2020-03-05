import csv

def dict_reader():
    with open('test.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row.keys())

def reader():
    with open('test.csv', 'rb') as f:
        reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            print(row)

reader()
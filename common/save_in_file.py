import csv
from settings import csv_delimiter


def create_new_file(filename, first_row):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=csv_delimiter)
        writer.writerow(first_row)


def add_to_file(filename, data):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=csv_delimiter)
        writer.writerows(data)

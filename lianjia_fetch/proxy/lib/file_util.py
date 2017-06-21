#! -*- encoding:utf-8 -*-
import csv


def save_csv(file_name, list_var, mode='a'):
    with open(file_name, mode) as f:
        writer = csv.writer(f, delimiter='\n')
        writer.writerow(list_var)


def test_csv():
    vars = set(['hello', '10.123.123.123:80', '88.123.123.123:80']);
    with open('dt.csv', 'wb') as f:
        writer = csv.writer(f, delimiter='\n')
        writer.writerow(list(vars))


def test_read_csv():
    with open('dt.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            print row[0]


def read_csv_to_list(csv_file, list_var):
    if csv_file is None:
        csv_file = 'dt.csv'
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 1:
                list_var.append(row[0])


def read_csv_to_queue(csv_file, proxy_queue):
    if csv_file is None:
        csv_file = 'dt.csv'
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 1:
                proxy_queue.put(row[0])

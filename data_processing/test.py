import csv
import matplotlib.pyplot as plt
import json
import os

def fill_hole(l, null_char=0):
    l = l.copy()
    num_1 = null_char
    num_1_index = 0
    num_2 = null_char
    num_2_index = 0
    done = False
    encountered_first = False
    i = 0
    while i < len(l):
        if l[i] != null_char:
            encountered_first = True
        if l[i] == null_char and encountered_first:
            if num_1_index == 0:
                num_1 = l[i - 1]
                num_1_index = i - 1
            j = 1
            while i + j < len(l):
                if l[i + j] != null_char:
                    num_2 = l[i + j]
                    num_2_index = i + j
                    done = True
                    break
                j += 1
            if done:
                break
        i += 1
    slope = (num_2 - num_1) / (num_2_index - num_1_index)
    i = num_1_index + 1
    while i < num_2_index:
        l[i] = num_1 + slope * (i - num_1_index)
        i += 1
    return l

def has_hole(l, null_char=0):
    i = 0
    new_start = 0
    new_end = 0
    while i < len(l):
        if l[i] != null_char:
            new_start = i
            break
        i += 1
    i = len(l) - 1
    while i >= 0:
        if l[i] != null_char:
            new_end = i + 1
            break
        i -= 1

    l = l[new_start:new_end + 1]
    i = 0
    while i < len(l):
        if l[i] == null_char:
            if i != 0 and i != len(l) - 1:
                return True
        i += 1
    return False

def fill_left_end(l, null_char=0):
    l = l.copy()
    num_1 = null_char
    num_1_index = 0
    num_2 = null_char
    i = 0
    while i < len(l):
        if l[i] != null_char:
            num_1 = l[i]
            num_1_index = i
            num_2 = l[i + 1]
            break
        i += 1
    slope = num_2 - num_1
    i = num_1_index - 1
    while i >= 0:
        l[i] = num_1 + slope * (i - num_1_index)
        i -= 1
    return l

def fill_right_end(l, null_char=0):
    l = l.copy()
    num_1 = null_char
    num_1_index = 0
    num_2 = null_char
    i = 0
    while i < len(l):
        if l[i] != null_char:
            num_1 = l[i]
            num_1_index = i
            num_2 = l[i + 1]
            break
        i += 1
    slope = num_2 - num_1
    i = num_1_index - 1
    while i < len(l):
        l[i] = num_1 + slope * (i - num_1_index)
        i += 1
    return l

def lin_interp(l, null_char=0):
    l = l.copy()
    num_non_null = 0
    last_non_null = 0
    null_pos = []

    j = 0
    for i in l:
        if i != null_char:
            last_non_null = i
            num_non_null += 1
        else:
            null_pos.append(j)
        j += 1

    if num_non_null == 1:
        j = 0
        while j < len(l):
            if l[j] == null_char:
                l[j] = last_non_null
            j += 1
    elif num_non_null == 0:
        return l
    else:
        m = 0
        while has_hole(l):
            l = fill_hole(l)
        if l[0] == null_char:
            l = fill_left_end(l)
        if l[len(l) - 1] == null_char:
            l = fill_right_end(l)

    return l


if __name__ == '__main__':

    if not os.path.exists('processed'):
        os.makedirs('processed')

    with open('raw/gini.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        countries = {}
        for row in csv_reader:
            if line_count == 0:
                pass
            else:
                countries[row[0]] = {'gini': lin_interp([float(n) / 100 if n != '' else 0 for n in row[1:-1]] if len(row[1:-1]) == 12 else [float(n) / 100 if n != '' else 0 for n in row[1:-1]] + [0])}
            line_count += 1

    lines = [['Country', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', ]]
    for c, k in zip(countries, countries.keys()):
        lines.append([c] + countries[k]['gini'])
    with open('processed/gini.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(lines)
    f.close()

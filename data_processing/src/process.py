import csv
import matplotlib.pyplot as plt
import json
import os
from utilities import lin_interp
import json

def combine_dict(base_dict, new_prop, prop_name):
    countries = base_dict.keys()
    for country in countries:
        base_dict[country][prop_name] = new_prop[country][prop_name]
    return base_dict

def read_csv_12_year(input_path, output_dir):
    name = input_path.split('/')[-1].split('.')[0]
    with open(os.path.join(input_path), 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        countries = {}
        for row in csv_reader:
            if line_count == 0:
                pass
            else:
                countries[row[0]] = {name: lin_interp([float(n.replace(',', '')) if n != '' else 0 for n in row[1:-1]] if len(row[1:-1]) == 12 else [float(n.replace(',', '')) if n != '' else 0 for n in row[1:-1]] + [0])}
            line_count += 1

    lines = [['Country', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', ]]
    for c, k in zip(countries, countries.keys()):
        lines.append([c] + countries[k][name])
    with open(os.path.join(output_dir, name + ".csv"), 'w') as f:
        writer = csv.writer(f)
        writer.writerows(lines)
    f.close()
    return countries

def read_csv_longlat(input_path, output_dir):
    name = input_path.split('/')[-1].split('.')[0]
    with open(os.path.join(input_path), 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        countries = {}
        for row in csv_reader:
            if line_count == 0:
                pass
            else:
                countries[row[0]] = {name: [float(n) for n in row[1:3]]}
            line_count += 1

    lines = [['Country', 'long', 'lat',]]
    for c, k in zip(countries, countries.keys()):
        lines.append([c] + countries[k][name])
    with open(os.path.join(output_dir, name + ".csv"), 'w') as f:
        writer = csv.writer(f)
        writer.writerows(lines)
    f.close()
    return countries

def read_csv_events(input_path):
    name = input_path.split('/')[-1].split('.')[0]
    with open(os.path.join(input_path), 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        events = []
        for row in csv_reader:
            if line_count < 2:
                pass
            else:
                data = {}
                data['country'] = row[1]
                data['year'] = int(row[2])
                data['displaced'] = int(row[7]) if row[7] != '' else 0
                data['displaced'] = data['displaced'] + (int(row[8]) if row[8] != '' else 0)
                events.append(data)
            line_count += 1
    return events

def add_country_data_to_events(events, countries):
    i = 0
    while i < len(events):
        try:
            countries[events[i]['country']]
        except KeyError:
            i += 1
            continue
        for key in countries[events[i]['country']].keys():
            if 'longlat' in key:
                events[i]['longitude'] = countries[events[i]['country']][key][1]
                events[i]['latitude'] = countries[events[i]['country']][key][0]
            else:
                events[i][key] = countries[events[i]['country']][key][events[i]['year'] - 2008]
        i += 1
    return events

if __name__ == '__main__':

    raw_dir = '../raw'
    processed_dir = '../processed'

    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    countries = 0

    raw_file_names = os.listdir(raw_dir)
    for raw_file_name in raw_file_names:
        if 'events' in raw_file_name:
            events = read_csv_events(os.path.join(raw_dir, raw_file_name))
        elif 'longlat' in raw_file_name:
            name = raw_file_name.split('.')[0]
            if countries == 0:
                countries = read_csv_longlat(os.path.join(raw_dir, raw_file_name), processed_dir)
            else:
                countries = combine_dict(countries, read_csv_longlat(os.path.join(raw_dir, raw_file_name), processed_dir), name)
        else:
            name = raw_file_name.split('.')[0]
            if countries == 0:
                countries = read_csv_12_year(os.path.join(raw_dir, raw_file_name), processed_dir)
            else:
                countries = combine_dict(countries, read_csv_12_year(os.path.join(raw_dir, raw_file_name), processed_dir), name)
    events = add_country_data_to_events(events, countries)

    with open(os.path.join(processed_dir, 'dataframe.json'), 'w') as json_file:
        json.dump(events, json_file)

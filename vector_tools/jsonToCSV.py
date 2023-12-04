import json
import csv
with open('data/beanieData.json') as json_file:
    data = json.load(json_file)

headers = data[0]['details'].keys()

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)        # init csvwriter
    writer.writerow(['name', 'url'] + list(headers))    # write top-level json row
    for item in data:                                   # write img & poem
        row = [item['name'], item['url']]
        details = item['details']
        row += [details['img'], details['poem']]
        print(row)
        if (details['poem'] != ""):
            writer.writerow(row)

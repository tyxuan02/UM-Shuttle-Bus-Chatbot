import json

with open('data.json') as data:
    data = json.load(data)

all_stops = []

for route in data['routes']:
    for stop in route['stops']:
        all_stops.append(stop)

all_stops = sorted(set(all_stops))
print(all_stops)
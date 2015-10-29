import numpy as np
import matplotlib.pyplot as plt

with open("Sacramentorealestatetransactions.csv", 'r') as f:
    content = f.readlines()

lines = content[0].split('\r')
keys  = lines[0].split(',')
data  = dict([[k, []] for k in keys])

for l in lines[1:]:
    for k, entry in zip(keys, l.split(',')):
        data[k].append(entry)

longitude = map(lambda x : float(x), data['longitude'])
latitude  = map(lambda x : float(x), data['latitude'])

plt.scatter(latitude, longitude)
plt.show()


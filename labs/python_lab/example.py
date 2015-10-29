from collections import defaultdict

s = 'mississipi'
m = defaultdict(int)
for c in s:
    m[c] += 1

print m


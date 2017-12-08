import sys

r = [chr(i) for i in range(1, 100000)]
print(r.index('А'), r.index('я')+1)
r = r[r.index('А'):r.index('я')+1] + [' ']

def form(s):
    e = [i.lower() for i in s if i in r]
    return ''.join(e).split()

t = []

for i in sys.stdin:
    try:
        t += form(i.strip())
    except:
        pass

print(t)
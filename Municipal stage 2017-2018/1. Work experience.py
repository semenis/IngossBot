inp = open('input.txt', 'r')
def input(): return inp.readline()
out = open('output.txt', 'w')
def print(s): return out.write(str(s))

a_, b_, c_ = 0, 0, 0

for i in range(int(input())):
    *name, date1, date2 = input().split()
    date1, date2 = list(map(int, date1.split('.'))), list(map(int, date2.split('.')))
    a, b, c = date2[0]-date1[0], date2[1]-date1[1], date2[2]-date1[2]
    if a < 0: b, a = b - 1, 30+a
    if b < 0:c, b = c-1, (360+(b*30))//30
    a += 1
    a_, b_, c_ = a_ + a, b_ + b, c_ + c 
    
r = a_//30
a_ = a-r*30
b_ += r

r = b_//12
b_ = b_-r*12
c_ += r

print('%s %s' % (c_, b_))

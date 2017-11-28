#
#  Решение на 100 баллов
#

inp = open('input.txt', 'r')
def input(): return inp.readline()
out = open('output.txt', 'w')
def print(s): return out.write(str(s))

root = []

m, n = map(int, input().split())
k = int(input())

for i in range(k):
    a, p = map(int, input().split())
    root.append((p, a))
    
res = 1024**256
    
for i in sorted(root):
    r = i[1]
    if m%r==0 and n%r==0:
        yet = i[0]*(m//r)*(n//r)
        if yet < res:
            res = yet
    
if res == 1024**256:
    print('no')
else:
    print(res)

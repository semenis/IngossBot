inp = open('input.txt', 'r')
def input(): return inp.readline()
out = open('output.txt', 'w')
def print(s): return out.write(str(s))

from functools import lru_cache
import threading

@lru_cache(10240)
def get_2(now, b, tryes, s):
    if now == b:
        return s
    if tryes > 6:
        return -1
    res = -1
    if now not in root:
        return -1
    if len(root[now]) > 5:
        for i in root[now][:5]:
            k = get_2(i[1], b, tryes+1, s + i[0])
            if k != -1:
                if res == -1:
                    res = k
                elif k < res:
                    res = k    
    else:
        for i in root[now]:
            k = get_2(i[1], b, tryes+1, s + i[0])
            if k != -1:
                if res == -1:
                    res = k
                elif k < res:
                    res = k          
    return res
    
@lru_cache(10240)
def get_1(now, b, tryes, s, CONST):
    if now == b:
        return s
    if tryes > 6:
        return -1
    res = -1
    if now not in root:
        return -1
    if len(root[now]) > 5:
        for i in root[now][:5]:
            if i[0] > CONST:
                continue
            k = get_1(i[1], b, tryes+1, s + i[0], CONST)
            if k != -1:
                if res == -1:
                    res = k
                elif k < res:
                    res = k
    else:
        for i in root[now]:
            if i[0] > CONST:
                continue
            k = get_1(i[1], b, tryes+1, s + i[0], CONST)
            if k != -1:
                if res == -1:
                    res = k
                elif k < res:
                    res = k
    return res

n, m, s = map(int, input().split())

res = {1:None, 2:None}

root = {}

for i in range(m):
    u, v, p = map(int, input().split())
    
    if u in root:
        root[u].append((p, v))
    else:
        root[u] = [(p, v)]
        
    if v in root:
        root[v].append((p, u))
    else:
        root[v] = [(p, u)]   
    
for i in root.items():
    root[i[0]] = list(sorted(i[1]))

def yet_1(now, b, tryes, s, CONST):
    res[1] = get_1(now, b, tryes, s, CONST)
    
def yet_2(now, b, tryes, s):
    res[2] = get_2(now, b, tryes, s)
    
a, b = map(int, input().split())

threading.Thread(target=yet_1, args=[a, b, 0, 0, s]).start()
threading.Thread(target=yet_2, args=[a, b, 0, 0]).start()

while res[1] == None or res[2] == None:
    pass

print('%s %s' % (res[1], res[2]))

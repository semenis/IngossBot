#
#  Решение на 100 баллов
#

inp = open('input.txt', 'r')
def input(): return inp.readline()
out = open('output.txt', 'w')
def print(s): return out.write(str(s))


from functools import lru_cache

@lru_cache(100000)
def check(s):
    res = s.replace('19', '').replace('28', '').replace('37', '').replace('46', '')
    return (res, res!=s)

n = int(input())

root = []

user1 = 0
user2 = 0

for i in range(0, n, 2):
    s = input().strip().replace('19', '').replace('28', '').replace('37', '').replace('46', '')
    while True:
        s = check(s)
        if not s[1]:
            s = s[0]
            break
        s = s[0]
    if s == '':
        user1 += 1000
        
    s = input().strip().replace('19', '').replace('28', '').replace('37', '').replace('46', '')
    while True:
        s = check(s)
        if not s[1]:
            s = s[0]
            break
        s = s[0]
    if s == '':
        user2 += 1000
    
print('%s:%s' % (user1, user2))

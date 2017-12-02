#
#  Solution on 41 balls
#

from functools import lru_cache

n, s = map(int, input().split())
ai = list(map(int, input().split()))

@lru_cache(maxsize=None)
def get(n):
    if n < 0:
        return 0
    else:
        return n

times = 0
ss = 0
while ss != s:
    times += 1
    ss = sum(map(lambda x: get(times-x), ai))

print(times)

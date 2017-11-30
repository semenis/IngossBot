#
#  Решение на 100 баллов
#


inp = open('input.txt', 'r')
def input(): return inp.readline()
out = open('output.txt', 'w')
def print(s): return out.write(str(s))


x0, y0, r = map(float, input().split())
x1, y1, x2, y2 = map(float, input().split())

AB = ((y1 - y2) ** 2 + (x1 - x2) ** 2) ** 0.5
AO = ((y1 - y0) ** 2 + (x1 - x0) ** 2) ** 0.5
BO = ((y0 - y2) ** 2 + (x0 - x2) ** 2) ** 0.5

s = (AO ** 2 - BO ** 2 + AB ** 2) / (2 * AB)
d = (AO ** 2 - s ** 2) ** 0.5
l = 2 * ((r ** 2 - d ** 2) ** 0.5)

print(round(l, 3))

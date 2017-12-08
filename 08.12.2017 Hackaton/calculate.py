# -*- coding: utf-8 -*-

class Calculate:
    def __init__(self):
        self.brackets = (40, 41)
        self.signs = (42, 43, 45, 47)
        self.all = (40, 41, 42, 43, 45, 47)

        self.additionally = {
            42: self.__mult__,
            43: self.__sum__,
            45: self.__diff__,
            47: self.__div__
        }

    def __sum__(self, a, b):
        return a + b

    def __diff__(self, a, b):
        d = -b.__len__()
        return a[:d] if b == a[d:] else a

    def __div__(self, a, b):
        d = len(b)
        if a[1::2][:d] == b:
            return a[::2] + a[d * 2 + 1:]
        return a

    def __mult__(self, a, b):
        d = min(len(a), len(b))
        return ''.join(map(lambda i: a[i] + b[i], range(d))) + a[d:] + b[d:]

    def __form__(self, s):
        return s.replace(chr(32), '')

    def __line__(self, s):
        nums, signs, yet, i = list(), list(), '', 0

        for elem in s:
            if ord(elem) in self.signs:
                nums.append(yet)
                signs.append(elem)
                yet = ''
            else:
                yet += elem
        nums.append(yet)

        while nums.__len__() > 1:
            if chr(42) in signs and chr(47) in signs:
                index = min(signs.index(chr(42)), signs.index(chr(47)))
            elif chr(42) in signs:
                index = signs.index(chr(42))
            elif chr(47) in signs:
                index = signs.index(chr(47))
            else:
                index = 0

            a, b = nums.pop(index), nums.pop(index)
            sign = ord(signs.pop(index))
            nums.insert(index, self.additionally[sign](a, b))

        return nums[0]

    def __brack__(self, s):
        while chr(41) in s:
            inx = s.index(chr(41))
            body = s[:inx]
            inx = (body.__len__() - body[::-1].index(chr(40)), inx)
            s = s[:inx[0] - 1] + self.__line__(body[inx[0]:]) + s[inx[1] + 1:]
        return self.__line__(s)

    def run(self, s):
        return self.__brack__(self.__form__(s))


c = Calculate()

text = '((index - ex) - d) + gst * osr + (an + k + oh) / (n + o)'
print('%s = %s' % (text, c.run(text)))

print()

text = input('Enter your expression: ')
print('%s = %s' % (text, c.run(text)))

>>> a = [2, 3, 5]
>>> b = [2, 3]
>>> a - b

Traceback (most recent call last):
  File "<pyshell#13>", line 1, in <module>
    a - b
TypeError: unsupported operand type(s) for -: 'list' and 'list'
>>> set(a) - set(b)
set([5])
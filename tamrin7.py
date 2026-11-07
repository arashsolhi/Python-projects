import sys

n = int(sys.argv[1])
v = 1
while v <= n//2:
    v *= 2

while v > 0:
    if n < v:
        print(0, end='')
    else:
        print(1, end='')
        n -= v
    v //= 2

print()
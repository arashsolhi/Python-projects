import sys
n = int(sys.argv[1])

total = 0 
for i in range(1, n + 1):
    total += 1.0 / i

print(total)
    
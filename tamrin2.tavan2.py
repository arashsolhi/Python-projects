import sys


n = sys.argv[1]
i = 1


while i <= int(n):
    
    power = 2 ** i
    i = i+1
    print(str(power))
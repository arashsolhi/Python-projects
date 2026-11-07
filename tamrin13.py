n = int(input("How many numbers? "))

total = 0
for i in range(n):
    num = int(input())
    total += num

print("Sum is", total)
total = 0.0
count = 0

print("Enter numbers :")

while True:
    value = input(f"Number {count + 1}: ")

    if value == "":
        break

    total += float(value)
    count += 1

if count > 0:
    avg = total / count
    print(f"Average is: {avg:.2f}")
else:
    print("No numbers entered.")
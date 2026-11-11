largest = 0
second_largest = 0

for i in range(5):
    num = int(input("Enter number: "))

    if num > largest:
        second_largest = largest
        largest = num
    elif num < largest and num > second_largest:
        second_largest = num

print("Largest       :", largest)
print("Second largest:", second_largest)
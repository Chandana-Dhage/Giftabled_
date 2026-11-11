rows = int(input("Enter rows: "))

for i in range(1, rows+1):
    for j in range(rows, i, -1):
        print(end=" ")
    for k in range(1, i+1):
        print(k, end=" ")
    print()
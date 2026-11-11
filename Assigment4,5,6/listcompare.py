marks = list(map(float, input("Enter marks separated by spaces: ").split()))
result = ["Pass" if mark >= 40 else "Fail" for mark in marks]
print(result)
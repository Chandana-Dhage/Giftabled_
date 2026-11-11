marks = []
for i in range(10):
    marks.append(float(input(f"Enter mark {i + 1}: ")))

print("Highest:", max(marks))
print("Lowest:", min(marks))
print("Average:", sum(marks) / len(marks))
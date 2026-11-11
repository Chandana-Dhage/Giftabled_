cities = ["Delhi", "Bangalore", "Mumbai"]
print("Initial:", cities)

new_city = input("City to add: ")
cities.append(new_city)

remove_city = input("City to remove: ")
if remove_city in cities:
    cities.remove(remove_city)
else:
    print("City not found")

print("Cities:", cities)
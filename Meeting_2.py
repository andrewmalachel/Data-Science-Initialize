grocery_list = ['Bread', 'Cereal', 'Peanut Butter']
print(grocery_list)

print(grocery_list[0])
print(grocery_list[1])
print(grocery_list[-1])

grocery_list.append('Sausage')
grocery_list.append('Croissant')
grocery_list.remove('Bread')
print(grocery_list)

grocery_list[1] = 'strawberry jam'
print(grocery_list)
print(len(grocery_list))

numbers = [4, 3, 9, 7, 5]
print(numbers)

numbers.sort()
print(numbers)

numbers.append(1)
numbers.append(2)
numbers.append(6)
numbers.append(8)
numbers.append(10)
print(numbers)

numbers.sort()
print(numbers)

grade_3 = numbers[:4]
print(grade_3)
grade_2 = numbers[4:7]
print(grade_2)
grade_1 = numbers[7:]
print(grade_1)

products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Mouse', 'Printer']
remove_product = products.pop(3)
print(f"Removed Product: {remove_product}")
print(f"List after removal: {products}")

temperature = [
    [25, 27, 28, 27],
    [23, 24, 26, 26],
    [24, 24, 27, 27],
    [22, 24, 25, 24],
]

print(temperature)
print(temperature[0])
print(temperature[0][0])

temperature.append([23, 24, 24, 26])
print(temperature)
print(len(temperature))
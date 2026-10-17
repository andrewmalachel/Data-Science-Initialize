age = input("Enter your age: ")

if age.isnumeric() and int(age) < 18:
    print("You are still underage.")
elif age.isnumeric() and int(age) >= 18 and int(age) < 65:
    print("You are an adult.")
elif age.isnumeric() and int(age) >= 65:
    print("You are a senior citizen.")
else:
    print("Invalid input. Please enter a valid age.")
allowance = 10
spending = 8

print(allowance > spending)
print(allowance < spending)
print(allowance != spending)
print(allowance == spending)

print((allowance == 10) and (spending == 8))
print((allowance == 10) or (spending == 5))

print("<->Practice Start<->")

Student_name = ["Alex", "Bryan", "Christ", "Dave", "Eva"]
Student_score = [100, 75, 80, 78, 99]
Student_grade = []

for i in Student_score:
    if i >= 90:
        Student_grade.append("A")
    elif i >= 80:
        Student_grade.append("B")
    else:
        Student_grade.append("C")

print(Student_grade)

print("<->Practice End<->")

print("<->Exercise Decision Making Start<->")

is_rainy = False
is_umbrella_exist = False

if is_rainy == False:
    print("Go to supermarket")
elif is_rainy == True and is_umbrella_exist == True:
    print("Take the Umbrella and go to supermarket")
else:
    print("Wait until the rain stops")

print("<->Exercise Decision Making End<->")

print("<->Practice Nested Conditions Start<->")

weather = input("How is the weather today? (sunny/rainy): ").lower()
time = input("What time is it? (morning/afternoon): ").lower()

if weather == "sunny":
    if time == "morning":
        activity = "Go Jogging."
    elif time == "afternoon":
        activity = "Play in the park."
    else:
        activity = "Invalid time input."
elif weather == "rainy":
    if time == "morning":
        activity = "read a book."
    elif time == "afternoon":
        activity = "watch a movie."
    else:
        activity = "Invalid time input."
else:
    activity = "Invalid weather input."

print("Suggested activity:", activity)

print("<->Exercise Grading System Start<->")

score = input("Enter the Exam Score: ")

if score.isnumeric() and int(score) >= 90 and int(score) <= 100:
    print("Your Score predicate is A")
elif score.isnumeric() and int(score) >= 80 and int(score) < 90:
    print("Your Score predicate is B")
elif score.isnumeric() and int(score) >= 70 and int(score) < 80:
    print("Your Score predicate is C")
elif score.isnumeric() and int(score) >= 60 and int(score) < 70:
    print("Your Score predicate is D")
elif score.isnumeric() and int(score) < 60:
    print("Your Score predicate is F(Remedial)")
else:
    print("Invalid input. Please enter a valid score.")

print("<->Exercise Grading System End<->")
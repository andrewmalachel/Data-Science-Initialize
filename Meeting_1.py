
# this is comment
"""
this is a multi-line comment
"""

movie_title = "Captain Marvel"
release_year = 2019
rating = 7.9
is_general_audience = False
print("The Movie Title is: " + movie_title)
print("Release Year is: " + str(release_year))
print("Rating is: " + str(rating))
print("Is General Audience: " + str(is_general_audience))

top_up_amount = 50 #besar nilai top up
count = 3 #berapa kali top up dilakukan
discount = 2 #besar diskon yang diberikan

"""
get total payment
"""
total_payment = top_up_amount * count
print("Total Payment: " + str(total_payment) + "$")

"""
total payment after discount
"""
total_discount = discount * count
payment_after_discount = total_payment - total_discount
print("Total Payment after Discount: " + str(payment_after_discount) + "$")



print ("""Burger Price List:
1. Beef Burger: $15 
2. Cheese Burger: $20
3. kids Burger: $9
""")
menu_price = input ("Menu Price: ") #harga menu nilainya berdasarkan input
amount = input ("Amount: ") #jumlah menu nilainya berdasarkan input
bill = int(menu_price) * int(amount) #total pembelian
print ("You need to pay: $" + str(bill))

First_Name = input("Your First Name: ")
Second_Name = input("Your Second Name: ")
Third_Name = input("Your Third Name: ")

Person_Info = input("Your Information: ")
Full_Name = First_Name + " " + Second_Name + " " + Third_Name
print("Your Full Name is: " + Full_Name)
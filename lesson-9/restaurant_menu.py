print "Welcome to the restaurant menu program."

menu = {}

while True:
    dish_name = raw_input("Please enter the name of the dish: ")
    dish_price = raw_input("Enter the price for '%s': " % dish_name)  # optionally you can transform price from string to float
    menu[dish_name] = dish_price

    new = raw_input("Would you like to enter new dish? (yes/no) ")

    if new.lower() == "no":
        break

print "Menu: %s" % menu

with open("menu.txt", "w+") as menu_file:
    for dish in menu:
        menu_file.write("%s, %s EUR\n" % (dish, menu[dish]))

print "Goodbye!"

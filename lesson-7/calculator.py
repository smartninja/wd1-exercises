# calculator example

x = int(raw_input("Enter the value for x: "))  # get user's input and convert it from string into integer (number)
print x

y = int(raw_input("Enter the value for y: "))  # get user's input and convert it from string into integer (number)
print y

operation = raw_input("Choose math operation (+, -, *, /: ")
print operation

if operation == "+":
    print x + y
elif operation == "-":
    print x - y
elif operation == "*":
    print x * y
elif operation == "/":
    print x / y
else:
    print"You did not provide the correct math operation."

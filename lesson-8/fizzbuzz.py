print "Welcome to the fizzbuzz game!"

end = raw_input("Please enter a number between 1 and 100: ")

try:
    end = int(end)

    for num in range(1, end+1):
        if num % 3 == 0 and num % 5 == 0:
            print "fizzbuzz"
        elif num % 3 == 0:
            print "fizz"
        elif num % 5 == 0:
            print "buzz"
        else:
            print num
except Exception as e:
    print "Please enter a whole number."

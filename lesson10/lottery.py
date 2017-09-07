import random


def generate_lottery_numbers(quantity):
    num_list = []

    while True:
        if len(num_list) == quantity:  # when the length of the list reaches the desired quantity, stop choosing new numbers
            break

        lot_num = random.randint(1, 50)

        if lot_num not in num_list:  # if the chosen number is not in the list yet, add it to it (this helps avoiding duplicates)
            num_list.append(lot_num)

    return num_list


def main():
    print "Welcome to the Lottery numbers generator."

    quantity_question = raw_input("Please enter how many random numbers would you like to have: ")

    try:
        quantity_num = int(quantity_question)
        print generate_lottery_numbers(quantity_num)
    except ValueError:
        print "Please enter a number."

    print "END."

if __name__ == "__main__":  # this means that if somebody ran this Python file, execute only the code below
    main()

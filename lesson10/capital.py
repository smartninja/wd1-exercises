import random


def main():
    country_capital_dict = {"Slovenia": "Ljubljana", "Croatia": "Zagreb", "Austria": "Vienna"}

    while True:
        random_num = random.randint(0, 2)
        selected_country = country_capital_dict.keys()[random_num]

        guess = raw_input("What is the capital of %s? " % selected_country)

        check_guess(guess, selected_country, country_capital_dict)

        again = raw_input("Would you like to continue this game? (yes/no) ")
        if again == "no":
            break

    print "END"
    print "_________________________"


def check_guess(user_guess, country, cc_dict):
    capital = cc_dict.get(country)  # get the selected country value from the dictionary

    if user_guess == capital:
        print "Correct! The capital of %s is indeed %s." % (country, capital)
        return True
    else:
        print "Sorry, you are wrong. The capital of %s is %s." % (country, capital)
        return False

if __name__ == "__main__":  # this means that if somebody ran this Python file, execute only the code below
    main()

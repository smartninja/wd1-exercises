#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


def main():
    secret = random.randint(1, 30)

    while True:
        guess = int(raw_input("Guess the secret number (between 1 and 30): "))

        if guess == secret:
            print "You guessed it - congratulations! It's number %s :)" % secret
            break
        elif guess > secret:
            print "Sorry, your guess is too high... Please try again."
        elif guess < secret:
            print "Sorry, your guess is too low... Please try again."


if __name__ == "__main__":
    main()

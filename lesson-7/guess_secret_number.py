#!/usr/bin/env python
# -*- coding: utf-8 -*-

secret = 22

guess = int(raw_input("Guess the secret number (between 1 and 30): "))

if guess == secret:
    print "You guessed it - congratulations! It's number 22 :)"
else:
    print "Sorry, your guess is not correct... Secret number is not " + str(guess)
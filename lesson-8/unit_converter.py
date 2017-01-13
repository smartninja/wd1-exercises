#!/usr/bin/env python
# -*- coding: utf-8 -*-

print "Hello! This is a unit converter that converts kilometers into miles."

while True:
    print "Please enter a number of kilometers that you'd like to convert into miles. Enter only a number!"
    km = raw_input("Kilometers: ")

    try:
        km = float(km.replace(",", "."))  # replace comma with dot, if user entered a comma

        miles = km * 0.621371

        print "{0} kilometers is {1} miles.".format(km, miles)
    except Exception as e:
        print "Please enter a number, not text!"

    choice = raw_input("Would you like to do another conversion (y/n): ")

    if choice.lower() != "y" and choice.lower() != "yes":
        break

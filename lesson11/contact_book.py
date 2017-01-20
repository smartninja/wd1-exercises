class Contact:
    def __init__(self, first_name, last_name, phone_number, birth_year, email):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.birth_year = birth_year
        self.email = email

    def get_full_name(self):
        return self.first_name + " " + self.last_name


def list_all_contacts(contacts):
    for index, person in enumerate(contacts):
        print "ID: " + str(index)  # index is an order number of the contact object in the contacts list
        print person.get_full_name()
        print person.birth_year
        print person.email
        print ""  # empty line

    if not contacts:
        print "You don't have any contacts in your contact list."


def add_new_contact(contacts):
    first_name = raw_input("Please enter contact's first name: ")
    last_name = raw_input("Please enter contact's last name: ")
    email = raw_input("Please enter contact's email address: ")
    phone = raw_input("Please enter contact's phone number: ")
    birth_year = raw_input("Please enter contact's birth year: ")

    new = Contact(first_name=first_name, last_name=last_name, phone_number=phone, birth_year=birth_year, email=email)
    contacts.append(new)

    print ""  # empty line
    print new.get_full_name() + " was successfully added to your contact list."


def edit_contact(contacts):
    print "Select the number of the contact you'd like to edit:"

    for index, person in enumerate(contacts):
        print str(index) + ") " + person.get_full_name()

    print ""  # empty line
    selected_id = raw_input("What contact would you like to edit? (enter ID number): ")
    selected_contact = contacts[int(selected_id)]

    new_email = raw_input("Please enter a new email address for %s: " % selected_contact.get_full_name())
    selected_contact.email = new_email

    print ""  # empty line
    print "Email updated."
    # ... you can do the same for other fields.


def delete_contact(contacts):
    print "Select the number of the contact you'd like to delete:"

    for index, person in enumerate(contacts):
        print str(index) + ") " + person.get_full_name()

    print ""  # empty line
    selected_id = raw_input("What contact would you like to delete? (enter ID number): ")
    selected_contact = contacts[int(selected_id)]

    contacts.remove(selected_contact)
    print ""  # empty line
    print "Contact was successfully removed from your contact list."


def main():
    print "Welcome to your Contact List"

    # let's add some contacts in our contact list so it's not empty
    john = Contact(first_name="John", last_name="Clark", phone_number="89348239429", birth_year="1979", email="john@clark.com")
    marissa = Contact(first_name="Marissa", last_name="Mayer", phone_number="83483204032", birth_year="1978", email="marissa@yahoo.com")
    bruce = Contact(first_name="Bruce", last_name="Wayne", phone_number="902432309443", birth_year="1939", email="bruce@batman.com")
    contacts = [john, marissa, bruce]

    while True:
        print ""  # empty line
        print "Please choose one of these options:"
        print "a) See all your contacts"
        print "b) Add a new contact"
        print "c) Edit a contact"
        print "d) Delete a contact"
        print "e) Quit the program."
        print ""  # empty line

        selection = raw_input("Enter your selection (a, b, c, d or e): ")
        print ""  # empty line

        if selection.lower() == "a":
            list_all_contacts(contacts)
        elif selection.lower() == "b":
            add_new_contact(contacts)
        elif selection.lower() == "c":
            edit_contact(contacts)
        elif selection.lower() == "d":
            delete_contact(contacts)
        elif selection.lower() == "e":
            print "Thank you for using Contact List. Goodbye!"
            break
        else:
            print "Sorry, I didn't understand your selection. Please try again."
            continue

if __name__ == "__main__":
    main()

"""
A terminal application for logging what work someone did on a certain day.
The data is collected in a CSV document
Author: Zachary Collins
Date: July, 2018
"""
import csv

import os

import re


# Creates the csv file if it doesn't exist already
try:
    file = open("log.csv", "r")
except IOError:
    with open("log.csv", "w") as csvfile:
        fieldnames = ['date', 'title', 'time spent', 'notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def clear_screen():
    """Clears the contents of the console"""

    os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    """Provides a menu on how to operate the program"""

    clear_screen()
    print("WORK LOG")
    print("What would you like to do?")
    print("a) Add new entry")
    print("b) Search in existing entries")
    print("c) Quit the program")


def run():
    """Runs the core function of the program"""

    menu()
    answer = input().lower()

    # Controls menu choice
    if answer == 'a':
        add_entry()
    elif answer == 'b':
        search()
    elif answer == 'c':
        pass


def add_entry():
    """Adds the entry to the CVS document"""

    clear_screen()
    date = input("Enter the Date \nPlease use MM/DD/YYYY: ")
    title = input("Enter the Title: ")
    if len(title) == 0:
        print("Must enter a Title")
        input("Press ENTER to try again")
        add_entry()
    try:
        time_spent = int(input("Enter the time spent (minutes): "))
    except ValueError:
        print("time spent must be a number")
        input("Press ENTER to try again")
        add_entry()
    notes = input("Enter any additional notes (Optional): ")
    clear_screen()

    with open("log.csv", "a") as csvfile:
        fieldnames = ['date', 'title', 'time spent', 'notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            'date': date,
            'title': title,
            'time spent': time_spent,
            'notes': notes,
            })

    input("Entry has been added. Press a key to return to menu. ")
    run()


def prompt():
    """Provides a menu on searching functions"""

    clear_screen()
    print("Search Options:")
    print("a) Find by Date")
    print("b) Find by Time Spent")
    print("c) Find by Exact Search")
    print("d) Find by Regex Pattern")


def search():
    """Controls the logic of how the user will seach entries"""

    prompt()
    answer = input().lower()

    if answer == 'a':
        find_date()
    elif answer == 'b':
        find_time()
    elif answer == 'c':
        find_exact()
    elif answer == 'd':
        find_regex()


def find_date():
    """Prompts the user to enter a valid date,
    allowing the user to choose an entry to view"""

    clear_screen()
    log = []
    dates = []
    with open('log.csv', newline='') as csvfile:
        line_reader = csv.reader(csvfile, delimiter='|')
        rows = list(line_reader)
        fields = str(rows[0])
        for row in rows[1:]:
            log.append(', '.join(row))
            for element in row:
                index = element.find(',')
                dates.append(element[0:index])
    print("The following are valid dates: ")
    for date in dates:
        print(date)
    search = input("\nEnter the Date (Must be valid)\nUse MM/DD/YYYY: ")
    counter = 0
    if search in dates:
        for row in log:
            if search in row:
                break
            counter += 1
    else:
        find_date()
    answer = 'n'
    while answer != 'v':
        clear_screen()
        print("Hit 'n' for next date \nHit 'v' to view the entries")
        print("\n" + dates[counter])
        answer = input()
        if answer == 'n':
            counter += 1
        if counter == len(dates):
            counter = 0
    clear_screen()
    print("Here are the entries of that date:")
    print(fields + "\n")
    count = 1
    for row in log:
        if dates[counter] in row:
            print("Entry {}: {}\n".format(count, row))
            count += 1
    input("Press a key to return to menu: ")
    run()


def find_time():
    """Prompts the user to enter a valid time,
    allowing the user to choose an entry to view"""

    clear_screen()
    log = []
    times = []
    with open('log.csv', newline='') as csvfile:
        line_reader = csv.reader(csvfile, delimiter='|')
        rows = list(line_reader)
        fields = str(rows[0])
        for row in rows[1:]:
            log.append(', '.join(row))
            for element in row:
                comma1 = element.find(',')
                comma2 = element.find(',', comma1 + 1)
                comma3 = element.find(',', comma2 + 1)
                times.append(element[comma2+1:comma3])
    print("The following are valid times: ")
    for time in times:
        print(time + " minutes")
    search = input("\nEnter the desired Time (Must be valid, Number only): ")
    counter = 0
    found = False
    for row in log:
        comma1 = row.find(',')
        comma2 = row.find(',', comma1 + 1)
        comma3 = row.find(',', comma2 + 1)
        if search in row[comma2+1:comma3]:
            found = True
            break
        counter += 1
    if not found:
        find_time()

    answer = 'n'
    while answer != 'v':
        clear_screen()
        print("Hit 'n' for next amount of time\nHit 'v' to view the entries")
        print("\n" + times[counter] + " minutes")
        answer = input()
        if answer == 'n':
            counter += 1
        if counter == len(times):
            counter = 0
    clear_screen()
    print("Here are the entries of that time")
    print(fields + "\n")
    count = 1
    for row in log:
        comma1 = row.find(',')
        comma2 = row.find(',', comma1 + 1)
        comma3 = row.find(',', comma2 + 1)
        if times[counter] in row[comma2+1:comma3]:
            print("Entry {}: {}\n".format(count, row))
            count += 1
    input("Press a key to return to menu: ")
    run()


def find_exact():
    """Prompts the user to enter a string to search for,
    providing all entries containing the string"""

    clear_screen()
    log = []
    title_notes = []
    with open('log.csv', newline='') as csvfile:
        line_reader = csv.reader(csvfile, delimiter='|')
        rows = list(line_reader)
        fields = str(rows[0])
        for row in rows[1:]:
            log.append(', '.join(row))
            for element in row:
                comma1 = element.find(',')
                comma2 = element.find(',', comma1 + 1)
                comma3 = element.find(',', comma2 + 1)
                title_notes.append(element[comma1+1:comma2] + " " +
                                   element[comma3+1:])
    print("The following are valid title/notes: ")
    for entry in title_notes:
        print(entry)
    search = input("\nEnter the string to search for (Must be valid): ")
    found = []
    count = 0
    for row in title_notes:
        if search in row:
            found.append(count)
        count += 1
    if len(found) == 0:
            answer = input("Error: string not in entries\npress 'ENTER'")
            find_exact()
    clear_screen()
    print(fields + "\n")
    counter = 1
    for entry in found:
        print("Entry {}: {}\n".format(counter, log[entry]))
        counter += 1
    input("Press a key to return to menu: ")
    run()


def find_regex():
    """Prompts the user to enter a Regex to search for,
    provides the entries with that regex"""

    clear_screen()
    log = []
    title_notes = []
    with open('log.csv', newline='') as csvfile:
        line_reader = csv.reader(csvfile, delimiter='|')
        rows = list(line_reader)
        fields = str(rows[0])
        for row in rows[1:]:
            log.append(', '.join(row))
            for element in row:
                comma1 = element.find(',')
                comma2 = element.find(',', comma1 + 1)
                comma3 = element.find(',', comma2 + 1)
                title_notes.append(element[comma1+1:comma2] + " " +
                                   element[comma3+1:])

    regex = input("Enter the desired Regular Expression to search for: ")
    count = 0
    found = []
    for row in title_notes:
        line = re.findall(r'{}'.format(regex), row)
        if len(line):
            found.append(count)
        count += 1
    counter = 1
    clear_screen()
    print(fields + "\n")
    for entry in found:
        print("Entry {}: {}".format(counter, log[entry]))
        counter += 1
    if len(found) == 0:
        print("No enties were found with that Regular Expression")
    input("Press a key to return to menu: ")
    run()


# Ensures this only runs upon the main method being called.
if __name__ == "__main__":
    run()


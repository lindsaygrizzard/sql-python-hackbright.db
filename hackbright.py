"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """
    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (
        row[0], row[1], row[2])


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]     #first thing user enters in shell
        args = tokens[1:]       #second through end of things user enters in shell
        print "I dont Quit!"

        if command == "student":
            github = args[0]    #zeroith spot in token 1 through end so its the second thing user enters in shell
            get_student_by_github(github)
            print "Access Student "

        if command == "project":
            #return all projects by title
            return_project_titles() 

        if command == "grades":
            #set second command line arg to the github name 
            student_github = args[0]
            project_title = args[1]
            return_grades(student_github, project_title) 
        
        if command == "new_grade":
            student_github, project_title, grade = args
            new_grade(student_github, project_title, grade)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

def return_project_titles():

    QUERY = """SELECT title FROM Projects"""
    db_cursor.execute(QUERY)
    titles = db_cursor.fetchall()
    print "Project Name: %s" % (titles)

def return_grades(student_github, project_title):

    QUERY = """SELECT grade, project_title FROM Grades WHERE student_github = ? AND project_title = ? """
    db_cursor.execute(QUERY, (student_github, project_title))
    grade = db_cursor.fetchall()
    print grade

def new_grade(student_github, project_title, grade):
    QUERY = """INSERT INTO Grades VALUES (?, ?, ?)  """
    db_cursor.execute(QUERY, (student_github, project_title, grade))
    db_connection.commit()
    print "Successfully added a(n) %s for %s on %s" % (grade, student_github, project_title)

def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.
    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """INSERT INTO Students VALUES (?, ?, ?) """
    db_cursor.execute(QUERY, (first_name, last_name, github))

    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)


if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()

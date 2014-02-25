import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row
#     return """\
# Student: %s %s
# Github account: %s"""%(row[0], row[1], row[2])

def make_new_student(first_name,last_name,github):
    query = """INSERT into Students (first_name, last_name, github) values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_project_by_title(title):
    query = """SELECT title, description, max_grade FROM Projects where title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Project: %s
Descrription: %s
Max Grade: %d"""%(row[0],row[1], row[2])

# def make_new_project(*args):
#     title = args[0]
#     description = ' '.join(args[1:-1])
#     max_grade = int(args[-1])
#     #print title, description, max_grade
#     query = """INSERT into Projects (title, description, max_grade) VALUES (?, ?, ?);"""
#     DB.execute(query, (title, description, max_grade))
#     CONN.commit()
#     print "Successfully added project: %s" % title

def make_new_project(title, description, max_grade):
    max_grade = int(max_grade)
    #print title, description, max_grade
    query = """INSERT into Projects (title, description, max_grade) VALUES (?, ?, ?);"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s" % title

def get_project_grade_by_github(title, github):
    query = """SELECT grade FROM Grades where project_title = ? and student_github = ?"""  
    DB.execute(query, (title, github))
    row = DB.fetchone()
    print """\
Project: %s
UserName: %s
Grade: %d"""% (title, github,row[0])

def show_all_grades_by_github(github):
    query = """ SELECT project_title, grade FROM Grades where student_github = ?"""
    DB.execute(query, (github,))
    # print "Showing all available grades for %s" % (github)
    # print  "Project       Grade"
    row = DB.fetchone()
    rows = []
    while row:
        rows.append(row)
        row = DB.fetchone()
    return rows


def give_grade_for_project(github, project, grade):
    grade = int(grade)
    query = """SELECT COUNT(*) FROM Projects WHERE title = ?"""
    DB.execute(query, (project,))
    row = DB.fetchone()
    if row[0] == 0:
        print "That project does not exist!"
        return

    query = """INSERT INTO Grades (student_github, project_title, grade) VALUES (?, ?, ?);"""
    DB.execute(query, (github, project, grade))
    CONN.commit()
    print "Successfully added grade %d for project %s by student %s" % (grade, project, github)

def get_grades_for_project(project):
    query = """SELECT student_github, grade FROM Grades where project_title = ?"""
    DB.execute(query, (project,))
    row = DB.fetchone()
    rows = []
    while row:
        rows.append(row)
        row = DB.fetchone()
    return rows

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()


def get_all_githubs():
    query = """SELECT github FROM Students;"""
    DB.execute(query)
    row = DB.fetchone()
    rows = []
    while row:
        rows.append(row)
        row = DB.fetchone()
    return rows

def get_all_projects():
    query = """SELECT title FROM Projects;"""
    DB.execute(query)
    row = DB.fetchone()
    rows = []
    while row:
        rows.append(row)
        row = DB.fetchone()
    return rows

def main():
    connect_to_db()
    command = None

    commands = {
        'student': ['github'],
        'new_student': ['first_name', 'last_name', 'github'],
        'project': ['title'],
        'new_project': ['title', 'description', 'max_grade'],
        'project_grade': ['title', 'github'],
        'assign_grade': ['github', 'project', 'grade'],
        'show_grades': ['github']
    }

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        command_args = commands.get(command)
        if command_args:
            if len(command_args) != len(args):
                print "You have not entered the correct number of arguments."
                print "Correct usage for %s:" % command
                print command_args
                continue
        else:
            print ('Valid commands:  student, new_student, project, new_project,\
project_grade, assign_grade, show_grades')
            continue


        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            get_project_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "project_grade":
            get_project_grade_by_github(*args)
        elif command == "assign_grade":
            give_grade_for_project(*args)
        elif command == "show_grades":
            show_all_grades_by_github(*args)
        else:
            print ('Valid commands:  student, new_student, project, new_project,\
             project_grade, assign_grade, show_grades')

    CONN.close()

if __name__ == "__main__":
    main()

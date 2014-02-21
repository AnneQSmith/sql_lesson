import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

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

def make_new_project(*args):
    title = args[0]
    description = ' '.join(args[1:-1])
    max_grade = int(args[-1])
    print title, description, max_grade
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


def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

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
        else:
            print ('Valid commands:  student, new_student, project, new_project')

    CONN.close()

if __name__ == "__main__":
    main()

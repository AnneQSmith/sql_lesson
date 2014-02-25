from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():

    hackbright_app.connect_to_db()
    githubs = hackbright_app.get_all_githubs()
    titles = hackbright_app.get_all_projects()

    hackbright_app.CONN.close()   
    return render_template("index.html", githubs=githubs, titles=titles)

@app.route("/create_student")
def create_student():
    return render_template("create_student.html")

@app.route("/create_project")
def create_project():
    return render_template("create_project.html")

@app.route("/new_project")
def new_project():
    hackbright_app.connect_to_db()

    title = request.args.get("title")
    description = request.args.get("description")
    max_grade = request.args.get("max_grade")
    hackbright_app.make_new_project(title=title, description=description, max_grade=max_grade)
    html = render_template("project_info.html", title=title, project_grades=[])

    hackbright_app.CONN.close()
    return html

@app.route("/add_grade")
def add_grade():

    hackbright_app.connect_to_db()

    title = request.args.get("title")
    githubs = hackbright_app.get_all_githubs()

    hackbright_app.CONN.close()
    return render_template("add_grade.html", title=title, githubs=githubs)

@app.route("/new_grade")
def new_grade():
    hackbright_app.connect_to_db()

    github = request.args.get("github")
    title = request.args.get("title")
    grade = request.args.get("grade")
    hackbright_app.give_grade_for_project(github, title, grade)
    project_grades = hackbright_app.get_grades_for_project(title)
    html = render_template("project_info.html", title = title, project_grades= project_grades)

    hackbright_app.CONN.close()
    return html


@app.route("/new_student")
def new_student():
    hackbright_app.connect_to_db()

    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    github = request.args.get("github")
    hackbright_app.make_new_student(first_name, last_name, github)
    html = render_template("student_info.html", first_name=first_name, last_name=last_name, github=github, grades=[])

    hackbright_app.CONN.close()
    return html

@app.route("/project")
def get_project():
    hackbright_app.connect_to_db()

    project_title = request.args.get("ptitle")
    #project = 

    project_grades = hackbright_app.get_grades_for_project(project_title)
    html = render_template("project_info.html", title = project_title, project_grades= project_grades)
    hackbright_app.CONN.close()
    return html

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    student = hackbright_app.get_student_by_github(student_github)
    grades = hackbright_app.show_all_grades_by_github(student_github)
    html = render_template("student_info.html", first_name=student[0],
                                                last_name=student[1],
                                                github=student[2], grades=grades)

    hackbright_app.CONN.close()  #CONN is global
    return html


if __name__ == "__main__":
    app.run(debug=True)



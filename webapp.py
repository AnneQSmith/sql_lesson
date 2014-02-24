from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/create_student")
def create_student():
    return render_template("create_student.html")

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



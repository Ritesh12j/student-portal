from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .extensions import db
from .models import Student

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/students")
def view_students():
    students = Student.query.all()
    return render_template("students.html", students=students)

@bp.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        new_student = Student(name=name, email=email)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for("main.view_students"))
    return render_template("add_students.html")

@bp.route("/api/students")
def students_json():
    students = Student.query.all()
    data = [{"id": s.id, "name": s.name, "email": s.email} for s in students]
    return jsonify(data)

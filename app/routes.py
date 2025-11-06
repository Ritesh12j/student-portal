from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from .extensions import db
from .models import Student

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    return render_template("index.html")

@bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

# JSON API - list students
@bp.route("/students", methods=["GET"])
def list_students():
    students = Student.query.order_by(Student.id).all()
    # if request wants HTML render the page
    if request.accept_mimetypes.accept_html and not request.accept_mimetypes.accept_json:
        return render_template("students.html", students=students)
    return jsonify([s.to_dict() for s in students])

# JSON API - add student via POST (JSON)
@bp.route("/students", methods=["POST"])
def add_student_api():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    course = data.get("course")
    if not name or not email:
        return jsonify({"error": "name and email required"}), 400

    # prevent duplicate email
    if Student.query.filter_by(email=email).first():
        return jsonify({"error": "email already exists"}), 400

    s = Student(name=name, email=email, course=course)
    db.session.add(s)
    db.session.commit()
    return jsonify(s.to_dict()), 201

# HTML form submit endpoint
@bp.route("/students/add", methods=["GET", "POST"])
def add_student_form():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        course = request.form.get("course")
        if not name or not email:
            flash("Name and Email are required.", "danger")
            return redirect(url_for("main.add_student_form"))

        if Student.query.filter_by(email=email).first():
            flash("Email already exists.", "warning")
            return redirect(url_for("main.add_student_form"))

        s = Student(name=name, email=email, course=course)
        db.session.add(s)
        db.session.commit()
        flash("Student added successfully.", "success")
        return redirect(url_for("main.list_students"))
    return render_template("add_student.html")

from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db, Student

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("register.html")

@main_bp.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    course = request.form.get("course")

    if not (name and email and phone and course):
        flash("Please fill all fields.", "danger")
        return redirect(url_for("main.home"))

    student = Student(name=name, email=email, phone=phone, course=course)
    db.session.add(student)
    db.session.commit()
    flash("Application submitted successfully!", "success")
    return render_template("success.html", name=name)

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Student

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == ADMIN_USER and request.form["password"] == ADMIN_PASS:
            session["admin"] = True
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid credentials.", "danger")
    return render_template("admin_login.html")

@admin_bp.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect(url_for("admin.login"))
    students = Student.query.all()
    return render_template("admin_dashboard.html", students=students)

@admin_bp.route("/update_status/<int:id>/<status>")
def update_status(id, status):
    if "admin" not in session:
        return redirect(url_for("admin.login"))
    student = Student.query.get_or_404(id)
    student.status = status
    db.session.commit()
    flash(f"Student {status} successfully.", "success")
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin.login"))

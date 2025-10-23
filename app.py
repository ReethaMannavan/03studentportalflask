from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from flask_mail import Mail, Message
from database import init_db

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Initialize DB
init_db()

# ---------------- EMAIL CONFIGURATION ---------------- #
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nisha.reetha30@gmail.com'
app.config['MAIL_PASSWORD'] = 'fris hfvj tbok ixrl'
app.config['MAIL_DEFAULT_SENDER'] = ('Vetri Tech Admissions', 'nisha.reetha30@gmail.com')

mail = Mail(app)

# ---------------- ROUTES ---------------- #

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    course = request.form['course']
    address = request.form['address']

    # Validation
    if not name.replace(" ", "").isalpha():
        flash("❌ Name should only contain letters.", "danger")
        return redirect(url_for('home'))
    if not phone.isdigit() or len(phone) != 10:
        flash("❌ Phone number must be exactly 10 digits.", "danger")
        return redirect(url_for('home'))

    conn = sqlite3.connect("student_portal.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO students (name, email, phone, course, address) VALUES (?, ?, ?, ?, ?)",
                    (name, email, phone, course, address))
        conn.commit()

        # Send email confirmation
        msg = Message(
            subject="🎓 Application Received - Vetri Tech Admissions",
            recipients=[email],
            body=f"Dear {name},\n\nYour application for {course} has been received successfully!\n\nBest regards,\nVetri Technology Solutions"
        )
        mail.send(msg)
        flash("✅ Application submitted successfully! Confirmation email sent.", "success")
    except sqlite3.IntegrityError:
        flash("❌ Email already registered!", "danger")
    except Exception as e:
        flash(f"⚠️ Error: {e}", "danger")
    finally:
        conn.close()

    return redirect(url_for('home'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("student_portal.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
        admin = cur.fetchone()
        conn.close()

        if admin:
            session['admin'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            flash("❌ Invalid credentials!", "danger")

    return render_template("admin_login.html")

@app.route('/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect("student_portal.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    conn.close()

    return render_template("admin_dashboard.html", students=students)

@app.route('/update_status/<int:student_id>/<string:new_status>')
def update_status(student_id, new_status):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect("student_portal.db")
    cur = conn.cursor()
    cur.execute("SELECT name, email, course FROM students WHERE id=?", (student_id,))
    student = cur.fetchone()
    cur.execute("UPDATE students SET status=? WHERE id=?", (new_status, student_id))
    conn.commit()
    conn.close()

    # Email notification
    if student:
        student_name, student_email, student_course = student
        subject = "✅ Application Approved" if new_status == "Approved" else "❌ Application Rejected"
        body = f"Dear {student_name},\n\nYour application for {student_course} has been {new_status.lower()}.\n\nRegards,\nVetri Technology Solutions"
        try:
            msg = Message(subject=subject, recipients=[student_email], body=body)
            mail.send(msg)
        except Exception as e:
            print("Email error:", e)

    flash(f"Status updated to {new_status}", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)

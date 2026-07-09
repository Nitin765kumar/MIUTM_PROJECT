import datetime
import random
import sqlite3

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    abort,
    jsonify
)

app = Flask(__name__)
app.secret_key = 'maurya_international_university_enterprise_secret_key_2026'
DATABASE_FILE = 'database/university.db'

import os

print("Database Path:", os.path.abspath(DATABASE_FILE))
# -----------------------------------------
# Helper Function
# -----------------------------------------

def generate_application_number():

    current_year = datetime.datetime.now().year

    random_number = random.randint(100000, 999999)

    return f"MIUTM-{current_year}-{random_number}"

# Database connection utility
def get_db_connection():
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection

# --- ROUTES ---

@app.route('/')
def index():
    connection = get_db_connection()
    try:
        bulletins = connection.execute('SELECT * FROM news_events ORDER BY id DESC LIMIT 3').fetchall()
        featured_courses = connection.execute('SELECT * FROM courses ORDER BY id ASC LIMIT 3').fetchall()
    finally:
        connection.close()
    return render_template('index.html', news=bulletins, courses=featured_courses)

@app.route('/about')
def about():
    connection = get_db_connection()
    try:
        faculty_board = connection.execute('SELECT * FROM faculty ORDER BY id ASC').fetchall()
    finally:
        connection.close()
    return render_template('about.html', faculty=faculty_board)

@app.route('/courses')
def courses():
    connection = get_db_connection()
    try:
        catalog = connection.execute('SELECT * FROM courses ORDER BY department ASC').fetchall()
    finally:
        connection.close()
    return render_template('courses.html', courses=catalog)

@app.route("/admission", methods=["GET", "POST"])
def admission():

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        father_name = request.form.get("father_name", "").strip()
        mother_name = request.form.get("mother_name", "").strip()

        gender = request.form.get("gender", "").strip()
        dob = request.form.get("dob", "").strip()

        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()

        category = request.form.get("category", "").strip()
        nationality = request.form.get("nationality", "").strip()

        qualification = request.form.get("qualification", "").strip()
        percentage = request.form.get("percentage", "").strip()

        course_name = request.form.get("course_name", "").strip()

        address = request.form.get("address", "").strip()
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()
        pincode = request.form.get("pincode", "").strip()

        remarks = request.form.get("remarks", "").strip()

        application_no = generate_application_number()

        connection = get_db_connection()

        try:

            connection.execute(
                """
                INSERT INTO admissions
                (
                    application_no,
                    full_name,
                    father_name,
                    mother_name,
                    gender,
                    dob,
                    email,
                    phone,
                    category,
                    nationality,
                    qualification,
                    percentage,
                    course_name,
                    address,
                    city,
                    state,
                    pincode,
                    remarks
                )
                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    application_no,
                    full_name,
                    father_name,
                    mother_name,
                    gender,
                    dob,
                    email,
                    phone,
                    category,
                    nationality,
                    qualification,
                    percentage,
                    course_name,
                    address,
                    city,
                    state,
                    pincode,
                    remarks
                )
            )

            connection.commit()

            # Last inserted Admission ID
            admission_id = connection.execute(
                "SELECT last_insert_rowid()"
            ).fetchone()[0]

            flash(
                f"Application verified. Reference: {application_no}",
                "success"
            )

            connection.close()

            return redirect(
                url_for(
                    "admission_success",
                    admission_id=admission_id
                )
            )

        except Exception as e:

            connection.rollback()

            print("Admission Error:", e)

            flash(
                "System execution failure. Please check input parameters.",
                "danger"
            )

            connection.close()

            return redirect(
                url_for("admission")
            )

    # -------------------------
    # GET Request
    # -------------------------

    connection = get_db_connection()

    try:

        available_programs = connection.execute(
            """
            SELECT course_name
            FROM courses
            ORDER BY course_name ASC
            """
        ).fetchall()

    finally:

        connection.close()

    return render_template(
        "admission.html",
        courses=available_programs
    )

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        connection = get_db_connection()
        try:
            connection.execute('''
                INSERT INTO contact_messages (name, email, subject, message)
                VALUES (?, ?, ?, ?)
            ''', (name, email, subject, message))
            connection.commit()
            flash("Message transmitted successfully to the registry.", "success")
        except Exception:
            connection.rollback()
            flash("Database network error. Unable to register message.", "danger")
        finally:
            connection.close()
            
        return redirect(url_for('contact'))
        
    return render_template('contact.html')

@app.route('/admin')
def admin():
    connection = get_db_connection()
    try:
        all_courses = connection.execute('SELECT * FROM courses ORDER BY id ASC').fetchall()
        all_admissions = connection.execute('SELECT * FROM admissions ORDER BY id DESC').fetchall()
        all_messages = connection.execute('SELECT * FROM contact_messages ORDER BY id DESC').fetchall()
    finally:
        connection.close()
    return render_template('admin.html', courses=all_courses, admissions=all_admissions, messages=all_messages)

# -------------------------------------------------------
# ADMISSION MANAGEMENT
# -------------------------------------------------------

@app.route("/admissions")
def admissions():

    connection = get_db_connection()

    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()

    query = "SELECT * FROM admissions WHERE 1=1"
    parameters = []

    # -------------------------
    # Search
    # -------------------------

    if search:

        query += """
        AND (
            application_no LIKE ?
            OR full_name LIKE ?
            OR phone LIKE ?
        )
        """

        keyword = f"%{search}%"
        parameters.extend([keyword, keyword, keyword])

    # -------------------------
    # Status Filter
    # -------------------------

    if status:

        query += " AND status = ?"
        parameters.append(status)

    query += " ORDER BY id DESC"

    all_admissions = connection.execute(
        query,
        parameters
    ).fetchall()

    total_applications = connection.execute(
        "SELECT COUNT(*) FROM admissions"
    ).fetchone()[0]

    pending_count = connection.execute(
        "SELECT COUNT(*) FROM admissions WHERE status='Pending'"
    ).fetchone()[0]

    review_count = connection.execute(
        "SELECT COUNT(*) FROM admissions WHERE status='Under Review'"
    ).fetchone()[0]

    approved_count = connection.execute(
        "SELECT COUNT(*) FROM admissions WHERE status='Approved'"
    ).fetchone()[0]

    rejected_count = connection.execute(
        "SELECT COUNT(*) FROM admissions WHERE status='Rejected'"
    ).fetchone()[0]

    course_list = connection.execute(
        "SELECT course_name FROM courses ORDER BY course_name ASC"
    ).fetchall()

    connection.close()

    return render_template(

        "admissions.html",

        admissions=all_admissions,

        total_applications=total_applications,

        pending_count=pending_count,

        review_count=review_count,

        approved_count=approved_count,

        rejected_count=rejected_count,

        search=search,

        status=status,

        courses=course_list

    )


# -------------------------------------------------------
# ADMISSION SUCCESS
# -------------------------------------------------------

@app.route("/admission/success/<int:admission_id>")
def admission_success(admission_id):

    connection = get_db_connection()

    admission = connection.execute(
        """
        SELECT *
        FROM admissions
        WHERE id = ?
        """,
        (admission_id,)
    ).fetchone()

    connection.close()

    if admission is None:

        flash("Admission record not found.", "danger")

        return redirect(url_for("admission"))

    return render_template(

        "admission_success.html",

        admission=admission

    )


# -------------------------------------------------------
# VIEW ADMISSION
# -------------------------------------------------------

@app.route("/admission/view/<int:admission_id>")
def view_admission(admission_id):

    connection = get_db_connection()

    admission = connection.execute(

        """
        SELECT *
        FROM admissions
        WHERE id = ?
        """,

        (admission_id,)

    ).fetchone()

    connection.close()

    if admission is None:

        flash("Admission record not found.", "danger")

        return redirect(url_for("admissions"))

    return render_template(

        "admission_view.html",

        admission=admission

    )

# -------------------------------------------------------
# TRACK ADMISSION
# -------------------------------------------------------

@app.route("/track-admission", methods=["GET", "POST"])
def track_admission():

    admission = None

    if request.method == "POST":

        application_no = request.form.get("application_no", "").strip()

        connection = get_db_connection()

        try:

            admission = connection.execute(

                """
                SELECT *
                FROM admissions
                WHERE application_no = ?
                """,

                (application_no,)

            ).fetchone()

        finally:

            connection.close()

        if admission is None:

            flash(

                "Application Number not found.",

                "danger"

            )

    return render_template(

        "track_admission.html",

        admission=admission

    )


# -------------------------------------------------------
# EDIT ADMISSION
# -------------------------------------------------------

@app.route("/admission/edit/<int:admission_id>", methods=["GET", "POST"])
def edit_admission(admission_id):

    connection = get_db_connection()

    if request.method == "POST":

        full_name = request.form["full_name"]
        father_name = request.form["father_name"]
        mother_name = request.form["mother_name"]
        gender = request.form["gender"]
        dob = request.form["dob"]
        email = request.form["email"]
        phone = request.form["phone"]
        category = request.form["category"]
        nationality = request.form["nationality"]
        qualification = request.form["qualification"]
        percentage = request.form["percentage"]
        course_name = request.form["course_name"]
        address = request.form["address"]
        city = request.form["city"]
        state = request.form["state"]
        pincode = request.form["pincode"]
        status = request.form["status"]
        remarks = request.form["remarks"]

        connection.execute(

            """
            UPDATE admissions
            SET
                full_name=?,
                father_name=?,
                mother_name=?,
                gender=?,
                dob=?,
                email=?,
                phone=?,
                category=?,
                nationality=?,
                qualification=?,
                percentage=?,
                course_name=?,
                address=?,
                city=?,
                state=?,
                pincode=?,
                status=?,
                remarks=?,
                updated_at=CURRENT_TIMESTAMP
            WHERE id=?
            """,

            (
                full_name,
                father_name,
                mother_name,
                gender,
                dob,
                email,
                phone,
                category,
                nationality,
                qualification,
                percentage,
                course_name,
                address,
                city,
                state,
                pincode,
                status,
                remarks,
                admission_id
            )

        )

        connection.commit()
        connection.close()

        flash(
            "Admission record updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "view_admission",
                admission_id=admission_id
            )
        )

    admission = connection.execute(

        "SELECT * FROM admissions WHERE id=?",

        (admission_id,)

    ).fetchone()

    courses = connection.execute(

        "SELECT course_name FROM courses ORDER BY course_name"

    ).fetchall()

    connection.close()

    if admission is None:

        abort(404)

    return render_template(

        "admission_edit.html",

        admission=admission,

        courses=courses

    )


# -------------------------------------------------------
# DELETE ADMISSION
# -------------------------------------------------------

@app.route("/admission/delete/<int:admission_id>")
def delete_admission(admission_id):

    connection = get_db_connection()

    try:

        admission = connection.execute(

            "SELECT id FROM admissions WHERE id=?",

            (admission_id,)

        ).fetchone()

        if admission is None:

            flash(
                "Admission record not found.",
                "danger"
            )

            return redirect(url_for("admissions"))

        connection.execute(

            "DELETE FROM admissions WHERE id=?",

            (admission_id,)

        )

        connection.commit()

        flash(
            "Admission record deleted successfully.",
            "success"
        )

    except Exception:

        connection.rollback()

        flash(
            "Unable to delete record.",
            "danger"
        )

    finally:

        connection.close()

    return redirect(url_for("admissions"))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
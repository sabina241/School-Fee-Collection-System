from flask import Flask, request, jsonify,render_template,session,redirect,url_for
from db import get_db_connection
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from flask import send_file
import io

app = Flask(__name__)
app.secret_key = "school_fee_secret_key"
# --------------------------------------------------
# ROUTES FOR FRONT END
# --------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/student/login")
def student_login_page():
    return render_template("student_login.html")


@app.route("/admin/login")
def admin_login_page():
    return render_template("admin_login.html")


@app.route("/student/signup")
def student_signup_page():
    return render_template("student_signup.html")


@app.route("/admin/signup")
def admin_signup_page():
    return render_template("admin_signup.html")

# --------------------------------------------------
# ROLE SELECTION
# --------------------------------------------------
@app.route("/select-role", methods=["POST"])
def select_role():
    role = request.json.get("role")

    if role not in ["student", "admin"]:
        return jsonify({"error": "Invalid role selected"}), 400

    return jsonify({
        "message": f"{role.capitalize()} selected",
        "next_step": f"/login/{role}"
    })


# --------------------------------------------------
# STUDENT SIGNUP
# --------------------------------------------------
@app.route("/signup/student", methods=["GET", "POST"])
def student_signup():
    if request.method == "GET":
        return render_template("student_signup.html")

    try:
        data = request.get_json()
        print("Received:", data)

        #Basic backend validation
        if not data.get("email") or not data["email"].endswith("@tcetmumbai.in"):
            return jsonify({"error": "Please provide a valid Gmail address"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Students
            (name, username, password, email, department, year_range, abc_id, blood_group)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["name"],
            data["username"],
            data["password"],
            data["email"].strip().lower(),
            data["department"],
            data["year_range"],
            data["abc_id"],
            data.get("blood_group")
        ))

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Student account created successfully",
            "redirect": "/login/student"
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

# --------------------------------------------------
# STUDENT LOGIN
# --------------------------------------------------
@app.route("/login/student", methods=["GET", "POST"])
def student_login():
    if request.method == "GET":
        return render_template("student_login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Students
        WHERE username = ? AND password = ?
    """, (username, password))

    student = cursor.fetchone()
    conn.close()

    if not student:
        return render_template(
            "student_login.html",
            error="Invalid username or password"
        )

    session["student_id"] = student[0]
    session["student_username"] = student[2]

    return redirect("/student/dashboard")

# --------------------------------------------------
# ADMIN SIGNUP
# --------------------------------------------------
@app.route("/signup/admin", methods=["GET", "POST"])
def admin_signup():
    if request.method == "GET":
        return render_template("admin_signup.html")

    try:
        data = request.get_json()
        print("ADMIN SIGNUP DATA:", data)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Admins (Name, Username, Password)
            VALUES (?, ?, ?)
        """, (
            data["name"],
            data["username"],
            data["password"]
        ))

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Admin account created successfully",
            "redirect": "/login/admin"
        })

    except Exception as e:
        print("ADMIN SIGNUP ERROR:", e)
        return jsonify({"error": str(e)}), 500

# --------------------------------------------------
# ADMIN LOGIN
# --------------------------------------------------
from flask import request, jsonify, render_template, session

@app.route("/login/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin_login.html")

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT AdminID, Name
        FROM Admins
        WHERE Username = ? AND Password = ?
    """, (username, password))

    admin = cursor.fetchone()
    conn.close()

    if not admin:
        return jsonify({"error": "Invalid admin credentials"}), 401

    #Store admin in session
    session["admin_id"] = admin.AdminID
    session["admin_name"] = admin.Name

    return jsonify({
        "redirect": "/admin/dashboard"
    })

# --------------------------------------------------
# FETCH STUDENT DETAILS
# --------------------------------------------------
@app.route("/student/profile/<username>", methods=["GET"])
def student_profile(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            name,
            username,
            department,
            year_range,
            abc_id,
            blood_group
        FROM Students
        WHERE username = ?
    """, (username,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Student not found"}), 404

    profile = {
        "name": row[0],
        "username": row[1],
        "department": row[2],
        "year_range": row[3],
        "abc_id": row[4],
        "blood_group": row[5]
    }

    return jsonify(profile)
# --------------------------------------------------
# STUDENT DASHBOARD
# --------------------------------------------------
@app.route("/student/dashboard")
def student_dashboard():
    if "student_id" not in session:
        return redirect("/login/student")
    username = session["student_username"]
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, username, department, year_range, abc_id, blood_group
        FROM Students
        WHERE username = ?
    """, (username,))

    student = cursor.fetchone()
    conn.close()

    if not student:
        return "Student not found"

    return render_template(
        "student_dashboard.html",
        student=student
    )
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -------------------------------
# PAY FEES PAGE
# -------------------------------
@app.route("/student/pay-fees")
def student_pay_fees_page():
    if "student_id" not in session:
        return redirect("/student/login")
    return render_template("student_pay_fees.html")

@app.route("/student/pay-fees/data")
def get_unpaid_fees():
    if "student_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    student_id = session["student_id"]
    filter_type = request.args.get("filter", "All")

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            f.FeeID,
            f.FeeName,
            ft.Frequency,
            f.Amount AS TotalAmount,
            ISNULL(SUM(p.AmountPaid), 0) AS PaidAmount,
            (f.Amount - ISNULL(SUM(p.AmountPaid), 0)) AS BalanceAmount
        FROM Students s
        JOIN Fees f
            ON s.department = f.Department
            AND s.year_range = f.YearRange
        JOIN FeeTypes ft
            ON f.FeeTypeID = ft.FeeTypeID
        LEFT JOIN Payments p
            ON p.FeeID = f.FeeID
            AND p.StudentID = s.student_id
        WHERE s.student_id = ?
    """

    params = [student_id]

    if filter_type in ["Yearly", "Half-Yearly", "Monthly"]:
        query += " AND ft.Frequency = ?"
        params.append(filter_type)

    query += """
        GROUP BY
            f.FeeID,
            f.FeeName,
            ft.Frequency,
            f.Amount
        HAVING (f.Amount - ISNULL(SUM(p.AmountPaid), 0)) > 0
        ORDER BY ft.Frequency
    """

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "fee_id": r[0],
            "fee_name": r[1],
            "type": r[2],
            "total": r[3],
            "paid": r[4],
            "balance": r[5]
        } for r in rows
    ])
@app.route("/student/pay-fees/pay", methods=["POST"])
def pay_fee():
    student_id = session["student_id"]
    data = request.json

    fee_id = data["fee_id"]
    amount = int(data["amount"])

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT f.Amount - ISNULL(SUM(p.AmountPaid),0)
        FROM Fees f
        LEFT JOIN Payments p
            ON f.FeeID = p.FeeID AND p.StudentID = ?
        WHERE f.FeeID = ?
        GROUP BY f.Amount
    """, (student_id, fee_id))

    balance = cursor.fetchone()[0]

    if amount <= 0 or amount > balance:
        return jsonify({"error": "Invalid amount"}), 400

    cursor.execute("""
        INSERT INTO Payments (StudentID, FeeID, AmountPaid)
        VALUES (?, ?, ?)
    """, (student_id, fee_id, amount))

    conn.commit()
    conn.close()

    return jsonify({"message": "Payment successful"})

# --------------------------------------------------
# PAYMENT HISTORY
# --------------------------------------------------
@app.route("/student/payment-history")
def payment_history():
    if "student_id" not in session:
        return redirect("/student/login")

    return render_template("payment_history.html")

@app.route("/student/payment-history/data")
def payment_history_data():
    student_id = session["student_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            f.FeeID,
            f.FeeName,
            ft.Frequency,
            f.Amount,
            SUM(p.AmountPaid),
            MAX(p.PaymentDate)
        FROM Payments p
        JOIN Fees f ON p.FeeID = f.FeeID
        JOIN FeeTypes ft ON f.FeeTypeID = ft.FeeTypeID
        WHERE p.StudentID = ?
        GROUP BY
            f.FeeID,
            f.FeeName,
            ft.Frequency,
            f.Amount
        HAVING SUM(p.AmountPaid) = f.Amount
        ORDER BY MAX(p.PaymentDate) DESC
    """, (student_id,))

    rows = cursor.fetchall()
    conn.close()

    return jsonify([
        {
            "fee_id": r[0],
            "fee_name": r[1],
            "type": r[2],
            "amount": r[3],
            "date": r[5].strftime("%d-%b-%Y")
        } for r in rows
    ])

@app.route("/student/receipt/<int:fee_id>")
def generate_receipt(fee_id):
    student_id = session["student_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.name,
            s.department,
            s.year_range,
            f.FeeName,
            ft.Frequency,
            f.Amount,
            MAX(p.PaymentDate)
        FROM Payments p
        JOIN Students s ON p.StudentID = s.student_id
        JOIN Fees f ON p.FeeID = f.FeeID
        JOIN FeeTypes ft ON f.FeeTypeID = ft.FeeTypeID
        WHERE p.StudentID = ? AND p.FeeID = ?
        GROUP BY
            s.name,
            s.department,
            s.year_range,
            f.FeeName,
            ft.Frequency,
            f.Amount
    """, (student_id, fee_id))

    data = cursor.fetchone()
    conn.close()

    if not data:
        return "Receipt not found", 404

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 800, "COLLEGE FEE RECEIPT")

    pdf.setFont("Helvetica", 12)
    y = 750

    labels = [
        ("Student Name", data[0]),
        ("Department", data[1]),
        ("Year Range", data[2]),
        ("Fee Name", data[3]),
        ("Fee Type", data[4]),
        ("Amount Paid", f"₹ {data[5]}"),
        ("Payment Date", data[6].strftime("%d-%b-%Y")),
        ("Status", "PAID")
    ]

    for label, value in labels:
        pdf.drawString(100, y, f"{label}:")
        pdf.drawString(260, y, str(value))
        y -= 30

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True,
                     download_name="fee_receipt.pdf",
                     mimetype="application/pdf")

# --------------------------------------------------
# ADMIN DASHBOARD
# --------------------------------------------------
@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        return redirect("/login/admin")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.student_id,
            s.name,
            s.department,
            f.FeeName,
            f.Amount,
            ISNULL(SUM(p.AmountPaid), 0) AS paid_amount,
            (f.Amount - ISNULL(SUM(p.AmountPaid), 0)) AS balance,
            CASE
                WHEN ISNULL(SUM(p.AmountPaid), 0) = 0 THEN 'Unpaid'
                WHEN ISNULL(SUM(p.AmountPaid), 0) >= f.Amount THEN 'Paid'
                ELSE 'Partial'
            END AS status
        FROM Students s
        JOIN Fees f
            ON s.department = f.Department
            AND s.year_range = f.YearRange
        LEFT JOIN Payments p
            ON s.student_id = p.StudentID
            AND f.FeeID = p.FeeID
        GROUP BY
            s.student_id,
            s.name,
            s.department,
            f.FeeName,
            f.Amount
    """)

    students = cursor.fetchall()

    cursor.execute("SELECT DISTINCT Department FROM Fees")
    departments = [row[0] for row in cursor.fetchall()]

    conn.close()

    return render_template(
        "admin_dashboard.html",
        admin_name=session["admin_name"],
        students=students,
        departments=departments
    )

@app.route("/admin/all-students")
def all_students():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT student_id, name, username, department FROM Students")
    rows = cursor.fetchall()

    students = []
    for r in rows:
        students.append({
            "id": r.student_id,
            "name": r.name,
            "username": r.username,
            "department": r.department
        })

    conn.close()
    return jsonify(students)

@app.route("/admin/remove-student/<int:student_id>", methods=["DELETE"])
def remove_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route("/logout/admin")
def admin_logout():
    session.clear()
    return redirect("/login/admin")


@app.route("/admin/api/stats")
def admin_stats_api():
    if "admin_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Revenue Health (Total Paid vs Total Pending)
    cursor.execute("""
        SELECT 
            SUM(f.Amount) as TotalExpected,
            ISNULL(SUM(p.AmountPaid), 0) as TotalPaid
        FROM Students s
        JOIN Fees f ON s.department = f.Department AND s.year_range = f.YearRange
        LEFT JOIN Payments p ON s.student_id = p.StudentID AND f.FeeID = p.FeeID
    """)
    res = cursor.fetchone()
    total_expected = res[0] or 0
    total_paid = res[1] or 0
    total_pending = total_expected - total_paid

    # 2. Department-wise Data
    cursor.execute("""
        SELECT 
            s.department, 
            ISNULL(SUM(p.AmountPaid), 0) as Paid
        FROM Students s
        LEFT JOIN Payments p ON s.student_id = p.StudentID
        GROUP BY s.department
    """)
    dept_rows = cursor.fetchall()

    conn.close()

    return jsonify({
        "revenue": {
            "paid": total_paid,
            "pending": total_pending
        },
        "departments": {row[0]: row[1] for row in dept_rows}
    })

# --------------------------------------------------
# RUN FLASK SERVER
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "appointment_tracker_secret_key"


# ---------------------------------------------------------------------------
# Database helper
# ---------------------------------------------------------------------------

def get_db_connection():
    """Create and return a MySQL database connection."""
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="appointment_tracker",
    )
    return connection


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    """Home page – shows a welcome message and navigation links."""
    return render_template("home.html")


@app.route("/appointments")
def view_appointments():
    """Display all appointments from the database."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM appointments ORDER BY appointment_date, appointment_time")
    appointments = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("appointments.html", appointments=appointments)


@app.route("/add", methods=["GET", "POST"])
def add_appointment():
    """Show form to add a new appointment and handle the form submission."""
    if request.method == "POST":
        patient_name = request.form["patient_name"]
        doctor_name = request.form["doctor_name"]
        appointment_date = request.form["appointment_date"]
        appointment_time = request.form["appointment_time"]
        reason = request.form["reason"]
        status = request.form["status"]

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO appointments
               (patient_name, doctor_name, appointment_date, appointment_time, reason, status)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (patient_name, doctor_name, appointment_date, appointment_time, reason, status),
        )
        connection.commit()
        cursor.close()
        connection.close()

        flash("Appointment added successfully!", "success")
        return redirect(url_for("view_appointments"))

    return render_template("add.html")


@app.route("/search", methods=["GET", "POST"])
def search_appointments():
    """Search appointments by patient name, doctor name, or date."""
    appointments = []
    search_query = ""
    if request.method == "POST":
        search_query = request.form["search_query"]
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """SELECT * FROM appointments
               WHERE patient_name LIKE %s
                  OR doctor_name  LIKE %s
                  OR appointment_date = %s
               ORDER BY appointment_date, appointment_time""",
            (f"%{search_query}%", f"%{search_query}%", search_query),
        )
        appointments = cursor.fetchall()
        cursor.close()
        connection.close()

    return render_template("search.html", appointments=appointments, search_query=search_query)


@app.route("/update/<int:appointment_id>", methods=["GET", "POST"])
def update_appointment(appointment_id):
    """Show a pre-filled form to update an appointment and handle submission."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        patient_name = request.form["patient_name"]
        doctor_name = request.form["doctor_name"]
        appointment_date = request.form["appointment_date"]
        appointment_time = request.form["appointment_time"]
        reason = request.form["reason"]
        status = request.form["status"]

        cursor.execute(
            """UPDATE appointments
               SET patient_name = %s, doctor_name = %s,
                   appointment_date = %s, appointment_time = %s,
                   reason = %s, status = %s
               WHERE id = %s""",
            (patient_name, doctor_name, appointment_date, appointment_time, reason, status, appointment_id),
        )
        connection.commit()
        cursor.close()
        connection.close()

        flash("Appointment updated successfully!", "success")
        return redirect(url_for("view_appointments"))

    cursor.execute("SELECT * FROM appointments WHERE id = %s", (appointment_id,))
    appointment = cursor.fetchone()
    cursor.close()
    connection.close()

    if appointment is None:
        flash("Appointment not found.", "danger")
        return redirect(url_for("view_appointments"))

    return render_template("update.html", appointment=appointment)


@app.route("/delete/<int:appointment_id>", methods=["POST"])
def delete_appointment(appointment_id):
    """Delete an appointment from the database."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
    connection.commit()
    cursor.close()
    connection.close()

    flash("Appointment deleted successfully!", "success")
    return redirect(url_for("view_appointments"))


# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)

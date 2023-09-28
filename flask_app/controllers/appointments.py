from flask_app import app
from flask import request, session, redirect, render_template
from flask_app.models.appointment import Appointment
from flask_app.models.user import User



@app.route("/appointments/edit/<int:appointment_id>")
def edit_appointment(appointment_id):
    data={
        'id' : appointment_id
    }
    return render_template("edit_appointment.html", details =Appointment.get_one_appointment(data))

@app.route("/process_update", methods=['POST'])
def process_update():
    data = {
        "id":request.form['id'],
        "task":request.form['task'],
        "date": request.form['date'],
        "status": request.form['status']
    }
    Appointment.update_appointment(data)
    return redirect('/appointments')



@app.route("/appointments/destroy/<int:appointment_id>")
def destroy_appointment(appointment_id):
    data ={
        'id' : appointment_id
    }
    Appointment.destroy_appointment(data)
    return redirect('/appointments')

@app.route("/appointments/add")
def new_appointment():
    return render_template("add_appointment.html")


@app.route("/process_appointment", methods=['POST'])
def process_appointment():
    if not Appointment.validate_user(request.form):
        # redirect to the route where the user form is rendered.
        return redirect('/appointments/add')
    # create the hash
    data = {
        "task":request.form['task'],
        "date":request.form['date'],
        "status": request.form['status'],
        "user_id": session['user_id']

    }
    id = Appointment.save(data)
    session['appointment_id'] = id
    is_valid = Appointment.validate_user(data)

    if is_valid:
        return redirect('appointments')

@app.route("/appointments")
def appointment():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("appointment.html", user = User.get_user_by_id(data), appointments= Appointment.get_all_appointments())




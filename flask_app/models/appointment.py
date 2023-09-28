from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash


class Appointment:
    def __init__(self, data):
        self.id = data["id"]
        self.task = data["task"]
        self.date = data["date"]
        self.status = data["status"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO appointments(task, date, status, user_id) VALUES (%(task)s, %(date)s, %(status)s, %(user_id)s);"
        return connectToMySQL("appointment").query_db(query, data)

    @classmethod
    def get_all_appointments(cls):
        query = "SELECT * FROM appointments;"
        appointments_from_db = connectToMySQL("appointment").query_db(query)
        appointments = []
        for a in appointments_from_db:
            appointments.append(cls(a))
        return appointments
    
    @classmethod
    def get_one_appointment(cls, data):
        query = "SELECT * FROM appointments WHERE id = %(id)s;"
        appointment_from_db = connectToMySQL("appointment").query_db(query, data)
        return cls(appointment_from_db[0])

    @classmethod
    def destroy_appointment(cls, data):
        query = "DELETE FROM appointments WHERE id = %(id)s;"
        return connectToMySQL("appointment").query_db(query, data)
    
    @classmethod
    def update_appointment(cls, data):
        query = "UPDATE appointments SET task=%(task)s, date=%(date)s, status=%(status)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL("appointment").query_db(query, data)
    

    @staticmethod
    def validate_user(appointment):
        is_valid = True  # Set the initial value to True
        if not appointment['task']:
            flash("Task field should have a value.", 'register')
            is_valid = False

        if not appointment['date']:
            flash("Date field should have a value.", 'register')
            is_valid = False

        if not appointment['status']:
            flash("Status field should have a value.", 'register')
            is_valid = False

        return is_valid
        
        

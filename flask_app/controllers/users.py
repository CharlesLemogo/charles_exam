from flask_app import app
from flask_bcrypt import Bcrypt  
from flask import render_template, redirect,request,session,flash
from flask_app.models.user import User
from flask_app.models.appointment import Appointment

bcrypt = Bcrypt(app)


@app.route('/')
def auth():
    return render_template('auth.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/process', methods=["POST"])
def process():
    if not User.validate_user(request.form):
        # redirect to the route where the user form is rendered.
        return redirect('/')
    # create the hash
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name":request.form['first_name'],
        "last_name":request.form['last_name'],
        "email": request.form['email'],
        "password": hashed_pw
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/appointments')


@app.route('/process-login', methods =['POST'])
def login_user():
    data = {
        'email':request.form['email']
    }
    
    user = User.get_user_by_email(data)
    if not user:
        flash("Invalid credentials", 'login')
        return redirect('/login')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid credentials", 'login')
        return redirect('/login')
    
    session['user_id'] = user.id
    return redirect('/appointments')




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
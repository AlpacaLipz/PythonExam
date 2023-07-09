from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.login_model import User
from flask_app.models.show_model import Show
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# =============== Login-Reg Landing ==========================

@app.route('/')
def alpaca():
    return render_template('login_reg.html')


# ============ Register - Action ===================

@app.route('/users/register', methods=['post'])
def user_register():
    if not User.validate(request.form):
        return redirect('/')
    # pass the hash man
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {**request.form, 'password' : pw_hash}

    user_id = User.create(data)
    # store the user_id of the created user in session
    session['user_id'] = user_id
    return redirect('/succ')

# ============== Dash Render ====================

@app.route('/succ')
def succ():

    #! ROUTE GUARD as long as your redirect isnt on the login page you can guard it
    if 'user_id' not in session:
        return redirect('/')
    # grab user_id from session
    data= {
        'id' : session['user_id']
    }
    all_shows = Show.get_all()
    logged_user = User.get_one_by_id(data)
    return render_template('success.html', logged_user = logged_user, all_shows = all_shows)

# ======== Log Out Button Render action ===========

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



# ============ Register Meth action ================

@app.route('/users/login', methods=['post'])
def vicuna():
    data = {
        'email' : request.form['email']
    }
    user_in_db = User.get_one_by_email(data)
    if not user_in_db:
        flash("WRONG!")
        return redirect('/')
    # not hashed passwords will come up as error something about salt and where to put it
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("WRONG!")
        return redirect('/')
    # else 
    session['user_id'] = user_in_db.id
    return redirect('/succ')



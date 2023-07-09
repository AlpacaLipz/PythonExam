from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.show_model import Show
from flask_app.models.login_model import User

# =========== show create render

@app.route('/shows/new')
def new_show():
    return render_template('create.html')

# ========= Create Meth Act (post) ===============

@app.route('/shows/make', methods=['post'])
def make_show():
    print(request.form)
    Show.validator(request.form)
    if not Show.validator(request.form):
        return redirect('/shows/new')
    
    show_data = {
        **request.form,
        'users_id' : session['user_id']
    }
    Show.create(show_data)
    return redirect('/succ')


# ============ Get One ================ 

@app.route('/shows/<int:id>')
def show_show(id):
    show_data = {
        'id' : id
    }
    return render_template('show_show.html', that_show = Show.get_one(show_data), logged_user = User.get_one_by_id({'id' : session['user_id']}))

# ============== Edit Update Render ===============================
@app.route('/shows/<int:id>/edit')
def shows_edit(id):
    return render_template('show_edit.html', that_show = Show.get_one({'id' : id}))

#============================ Edit Meth Act ==============================================
@app.route('/shows/<int:id>/update', methods=['post'])
def update_show(id):
    if not Show.validator(request.form):
        return redirect(f"/shows/{id}/edit")
    update_data = {
        **request.form,
        'id' : id
    }
    Show.update_show(update_data)
    return redirect('/succ')

# ================= Delete Route ==================== 
@app.route("/shows/<int:id>/delete")
def delete(id):
    Show.delete({'id' : id})
    return redirect("/succ")


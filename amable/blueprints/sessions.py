from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_user

from amable.models.user import User
from amable import session, login_manager

from ..forms.login_form import LoginForm

from amable.utils.password import check_password
from amable.utils.misc import flash_errors

sessions = Blueprint('sessions', __name__,
                     template_folder='../templates/sessions')


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).filter_by(id=user_id).first()


@sessions.route('/login', methods=['GET'])
def login():
    login_form = LoginForm()
    return render_template('login.html', form=login_form)


@sessions.route('/sessions/create', methods=['POST'])
def create():
    # email 'variable' is the column. request.form['email'] is the post data
    print("email provided : " + request.form['email'])
    user = session.query(User).filter_by(email=request.form['email']).first()

    # Does the user exist from the query done above?
    if user is None:
        flash("No User Found")
        return redirect('/login')
    else:
        # testing
        print("create() ~ User Password : " + user.password)
        print("create() ~ Username : " + user.username)

    form = LoginForm()

    if form.validate_on_submit():
        print("Form validated")
        if check_password(user, request.form["password"]):
            print("password checked good to go")
            login_user(user)
            flash("Login Successful")
            return redirect("/")
        else:
            flash("Login Credentials are wrong")
            return redirect('/login')
    else:
        flash_errors(form)
        flash("Login format wrong")
        return redirect('/login')

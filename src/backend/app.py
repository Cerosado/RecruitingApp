from functools import wraps
from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from forms import RegisterForm, LoginForm
from DAOs.userDAO import UserDao
from Handlers import jobPosting

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'ciic4060'


@app.route('/jobposting/<int:posting_id>', methods=['GET'])
def jobPostingDetail(posting_id):
    if request.method == 'GET':
        return jobPosting.getRankedApplicationsByJobPostingId(posting_id)
    else:
        return jsonify(Error="Method not allowed"), 405

@app.route('/jobposting/<int:uid>', methods=['GET'])
def jobPostings(uid):
    if request.method == 'GET':
        return jobPosting.getJobPostingsByUserId(uid)
    else:
        return jsonify(Error="Method not allowed"), 405

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please log in.', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def home():
    #to change to whatever home is in react
    return render_template('home.html')


@app.route('/applications')
@is_logged_in
def applications():
    #go to account settings with user_ID, not home
    return render_template('home.html')
@app.route('/jobPostings')
@is_logged_in
def jobPostings():
    #go to account settings with user_ID, not home
    return render_template('home.html')

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash("You are now logged out.", "success")
    return redirect(url_for('home'))

@app.route('/login')
@app.route('/login', methods=['GET', 'POST'])
def login():
    dao = UserDao()
    form = LoginForm(request.form)
    if request.method == 'POST':
        # Get form fields
        username = form.username.data
        password_candidate = form.password.data
        user = dao.getUserByUsername(username)
        if user:
            # Get stored hash
            password = user['password']
            # Compare passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['user_id'] = user['user_id']
                session['is_recruiter'] = user['is_recruiter']
                flash('You are now logged in.', 'success')
                if(session['is_recruiter']):
                    return redirect(url_for('jobPostings'))
                return redirect(url_for('applications'))
            else:
                error = 'Invalid login.'
            return render_template('login.html', form=form, error=error)
        else:
            error = 'Username not found.'
            return render_template('login.html', form=form, error=error)

    return render_template('login.html', form=form)

@app.route('/register/<isApplicant>', methods=['GET', 'POST'])
def register(isApplicant):
    dao = UserDao()
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        first_name = form.firstName.data
        last_name = form.lastName.data
        email = form.email.data
        username = form.username.data
        is_recruiter = form.isRecruiter.data
        password = sha256_crypt.encrypt(str(form.password.data))
        dao.registerUser(username, password, first_name, last_name, email, is_recruiter)
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('home'))
    if(isApplicant):
        form.isRecruiter.data='FALSE'
        #This template doesn't ask for last name, name is changed to Company.
        return render_template('registerApplicant.html', form=form)
    form.isRecruiter.data='TRUE'
    form.lastName.data=''
    return render_template('registerRecruiter.html', form=form)

if __name__ == '__main__':
    app.run()
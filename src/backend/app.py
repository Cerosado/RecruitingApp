from io import BytesIO
from functools import wraps
from flask import Flask, request, flash, redirect, url_for, session, jsonify
from flask_cors import CORS
# from passlib.hash import sha256_crypt
# from wtforms import Form, StringField, TextAreaField, PasswordField, validators
# from forms import RegisterForm, LoginForm
from src.backend.Handlers.jobPosting import JobPostingHandler
from src.backend.Handlers.resume import ResumeHandler
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'ciic4060'


@app.route('/JobPosting/<int:posting_id>', methods=['GET'])
def jobPostingDetail(posting_id):
    if request.method == 'GET':
        return JobPostingHandler().getRankedApplicationsByJobPostingId(posting_id)
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/JobPosting', methods=['GET'])
def jobPostings():
    user_id = request.args.get('user_id')
    if request.method == 'GET' and user_id:
        return JobPostingHandler().getJobPostingsByUserId(user_id)
    else:
        return jsonify(Error="Method not allowed"), 405


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ('pdf', 'doc', 'docx')


@app.route('/Applications', methods=['POST'])
def parse_resume():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify(Error="File error")
        file = request.files['file']
        if file.filename == '':
            return jsonify(Error="File error")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if filename:
                resume = BytesIO(file.read())
                resume.name = filename
                return ResumeHandler().parse_and_rank_resume(
                    resume,
                    skills_file='./resume_parser/skills_dataset.csv')
            return jsonify(Error="Filename not secure")
    return jsonify(Error="Method not allowed")


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please log in.', 'danger')
            return redirect(url_for('login'))
    return wrap


# @app.route('/logout')
# @is_logged_in
# def logout():
#     session.clear()
#     flash("You are now logged out.", "success")
#     return redirect(url_for('home'))
#
# @app.route('/login')
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     dao = UserDao()
#     form = LoginForm(request.form)
#     if request.method == 'POST':
#         # Get form fields
#         username = form.username.data
#         password_candidate = form.password.data
#         user = dao.getUserByUsername(username)
#         if user:
#             # Get stored hash
#             password = user['password']
#             # Compare passwords
#             if sha256_crypt.verify(password_candidate, password):
#                 # Passed
#                 session['logged_in'] = True
#                 session['username'] = username
#                 session['user_id'] = user['user_id']
#                 session['is_recruiter'] = user['is_recruiter']
#                 flash('You are now logged in.', 'success')
#                 if(session['is_recruiter']):
#                     return redirect(url_for('jobPostings'))
#                 return redirect(url_for('applications'))
#             else:
#                 error = 'Invalid login.'
#             return render_template('login.html', form=form, error=error)
#         else:
#             error = 'Username not found.'
#             return render_template('login.html', form=form, error=error)
#
#     return render_template('login.html', form=form)
#
# @app.route('/register/<isApplicant>', methods=['GET', 'POST'])
# def register(isApplicant):
#     dao = UserDao()
#     form = RegisterForm(request.form)
#     if request.method == 'POST' and form.validate():
#         first_name = form.firstName.data
#         last_name = form.lastName.data
#         email = form.email.data
#         username = form.username.data
#         is_recruiter = form.isRecruiter.data
#         password = sha256_crypt.encrypt(str(form.password.data))
#         dao.registerUser(username, password, first_name, last_name, email, is_recruiter)
#         flash('You are now registered and can log in', 'success')
#         return redirect(url_for('home'))
#     if(isApplicant):
#         form.isRecruiter.data='FALSE'
#         #This template doesn't ask for last name, name is changed to Company.
#         return render_template('registerApplicant.html', form=form)
#     form.isRecruiter.data='TRUE'
#     form.lastName.data=''
#     return render_template('registerRecruiter.html', form=form)


if __name__ == '__main__':
    app.run()

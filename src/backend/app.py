from functools import wraps
from io import BytesIO

import flask_praetorian
import flask_sqlalchemy
from flask import Flask, request, flash, redirect, url_for, session, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from .Handlers.jobPosting import JobPostingHandler
from .Handlers.resume import ResumeHandler

guard = flask_praetorian.Praetorian()

# Initialize flask
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'top secret'
app.config["JWT_ACCESS_LIFESPAN"] = {"hours": 24}
app.config["JWT_REFRESH_LIFESPAN"] = {"days": 30}

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://gbxrvscvbgnrfj:b4b81ffde7b3f9148b3bdc017063c4c706bef179663a188dedae12f22aa5a13f@' \
    'ec2-18-209-187-54.compute-1.amazonaws.com:5432/d99l1bhk1b777a'
db = flask_sqlalchemy.SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)


# SQLAlchemy model used by flask-praetorian to access accounts table
class User(db.Model):
    __table__ = db.Model.metadata.tables['accounts']

    @property
    def identity(self):
        return self.user_id

    @property
    def rolenames(self):
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    def is_valid(self):
        return self.is_active


# Initialize the flask-praetorian instance for the app
guard.init_app(app, User)


###########################################
#             Job Postings                #
###########################################
@app.route('/JobPosting/<int:posting_id>', methods=['GET'])
@flask_praetorian.roles_required("recruiter")
def jobPostingDetail(posting_id):
    if request.method == 'GET':
        return JobPostingHandler().getRankedApplicationsByJobPostingId(posting_id)
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/JobPosting', methods=['GET'])
@flask_praetorian.roles_required("recruiter")
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
                    resume_file=resume, resume_filename=filename,
                    skills_file='./resume_parser/skills_dataset.csv',
                    form=request.form)
            return jsonify(Error="Filename not secure")
    return jsonify(Error="Method not allowed")


###########################################
#             Authentication              #
###########################################
@app.route('/api/login', methods=['POST'])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/api/login -X POST \
         -d '{"username":"Yasoob","password":"strongpassword"}'
    """
    req = request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return ret, 200


@app.route('/api/refresh', methods=['POST'])
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refrehsed access expiration.
    .. example::
       $ curl http://localhost:5000/api/refresh -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    print("refresh request")
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}
    return ret, 200


@app.route('/api/protected')
@flask_praetorian.roles_required("applicant")
def protected():
    """
    A protected endpoint. The auth_required decorator will require a header
    containing a valid JWT
    .. example::
       $ curl http://localhost:5000/api/protected -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    return jsonify(message=f'protected endpoint (allowed user {flask_praetorian.current_user().username})')


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

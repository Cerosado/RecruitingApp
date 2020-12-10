import os
from functools import wraps
from io import BytesIO
import flask_praetorian
import flask_sqlalchemy
from flask import Flask, request, flash, redirect, url_for, session, jsonify
from flask_cors import CORS
from flask_mail import Mail
from werkzeug.utils import secure_filename
import sys
import base64

from backend.Handlers.applications import ApplicationsHandler
from .Handlers.jobPosting import JobPostingHandler
from .Handlers.user import UserHandler
from .Handlers.resume import ResumeHandler
from .Handlers.models import ModelsHandler

guard = flask_praetorian.Praetorian()

# Initialize flask
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME', None),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD', None),
    MAIL_DEFAULT_SENDER=os.environ.get('MAIL_USERNAME', None),
    MAIL_DEBUG=True,
    MAIL_SUPPRESS_SEND=False
)
Mail(app)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'top secret'
app.config["JWT_ACCESS_LIFESPAN"] = {"hours": 24}
app.config["JWT_REFRESH_LIFESPAN"] = {"days": 30}
app.config["PRAETORIAN_CONFIRMATION_SENDER"] = os.environ.get('MAIL_USERNAME', None)


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

@app.route('/Profile', methods=['GET'])
@flask_praetorian.auth_required
def userDetail():
    if request.method == 'GET':
        current_user=flask_praetorian.current_user()
        user=UserHandler().getUsersById(current_user.user_id)
        return user
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/update/email', methods=['POST'])
@flask_praetorian.auth_required
def updateEmail():
    if request.method == 'POST':
        current_user=flask_praetorian.current_user()
        UserHandler().editUser({'email':request.get_json(force=True).get("email","NONE FOUND")},current_user.user_id)
        return "Email posted!"
    else:
        return jsonify(Error="Method not allowed"), 405

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


@app.route('/JobPosting', methods=['GET', 'POST'])
@flask_praetorian.roles_accepted("recruiter", "applicant")
def jobPostings():
    user_id = flask_praetorian.current_user().identity
    if request.method == 'GET' and user_id:
        if (flask_praetorian.current_user().rolenames[0] == 'recruiter'):
            return JobPostingHandler().getJobPostingsByUserId(user_id)
        else:
            view = JobPostingHandler().getAllJobPostings()
            return view
    else:
        return jsonify(Error="Method not allowed"), 405
@app.route('/JobPostingForm', methods=['POST'])
@flask_praetorian.roles_required("recruiter")
def jobPostingForm():
    user_id = flask_praetorian.current_user().identity
    if request.method == 'POST' and user_id:
        return JobPostingHandler().createJobPosting(request.get_json(force=True), user_id)
    else:
        return jsonify(Error="Method not allowed"), 405

@app.route('/JobPostingForm/<int:posting_id>', methods=['GET'])
@flask_praetorian.roles_required("applicant")
def getJobPosting(posting_id):
    user_id = flask_praetorian.current_user().identity
    if request.method == 'GET' and user_id:
        test = JobPostingHandler().getJobPostingById(posting_id)
        return test
    else:
        return jsonify(Error="Method not allowed"), 405

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ('pdf', 'doc', 'docx')


@app.route('/Models', methods=['GET'])
@flask_praetorian.roles_required("recruiter")
def get_fields_of_work():
    if request.method == 'GET':
        return ModelsHandler().get_all_models()
    else:
        return jsonify(Error="Method not allowed"), 405


###########################################
#        Resumes and Applications         #
###########################################

@app.route('/Applications', methods=['GET'])
@flask_praetorian.roles_accepted("applicant")
def applications():
    user_id = flask_praetorian.current_user().identity
    if request.method == 'GET' and user_id:
        return ApplicationsHandler().getApplicationsByUserId(user_id)
    else:
        return jsonify(Error="Method not allowed"), 405

@app.route('/Applications/<int:posting_id>', methods=['POST'])
@flask_praetorian.roles_required("applicant")
def create_application(posting_id):
    if request.method == 'POST':
        user_id = flask_praetorian.current_user().identity
        return ApplicationsHandler().createApplication(user_id, posting_id)
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Resumes', methods=['GET','POST'])
@flask_praetorian.roles_required("applicant")
def parse_resume():
    if request.method == 'POST':
        print(request.files, file=sys.stderr)
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
                return ResumeHandler().parse_resume(
                    resume_file=resume, resume_filename=filename,
                    skills_file='./resume_parser/skills_dataset.csv')
            return jsonify(Error="Filename not secure")
    if request.method == 'GET':
        resume = ResumeHandler().getResumeByUserId(flask_praetorian.current_user().user_id)
        if(resume):
            #just send the essentials
            b64Data=base64.b64encode(resume['resume_data'].tobytes())
            data = b64Data.decode('utf-8')
            ext=resume['resume_extension']
            applicantResume = {'resume_data':data,'resume_extension':ext}
            return applicantResume
        return jsonify(Error="Resource not found")
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


@app.route('/api/register', methods=['POST'])
def register():
    req = request.get_json(force=True)
    first_name = req.get('firstName', None)
    last_name = req.get('lastName', None)
    username = req.get('username', None)
    email = req.get('email', None)
    password = req.get('password', None)
    is_company = req.get('isCompany', None)
    # TODO: Validate fields
    if User.query.filter_by(username=username).one_or_none() or \
            User.query.filter_by(email=email).one_or_none():
        return jsonify(Error='Account with same username or email already exists'), 409
    else:
        validate_email = os.environ.get('EMAIL_VALIDATION', 0) == 1
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=guard.hash_password(password),
            is_recruiter=is_company,
            roles='recruiter' if is_company else 'applicant',
            is_active=not validate_email,
        )
        db.session.add(new_user)
        db.session.commit()
        if validate_email:
            guard.send_registration_email(
                email=email, user=new_user, confirmation_uri='http://localhost:3000/Auth/Confirm'
            )
        result_message = 'successfully sent registration email to user {}' if validate_email else \
            'successfully registered user {}'
        ret = {'message': result_message.format(new_user.username)}
        return jsonify(ret), 201


@app.route('/finalize', methods=['POST'])
def finalize():
    """
    Finalizes a user registration with the token that they were issued in their
    registration email
    .. example::
       $ curl http://localhost:5000/finalize -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    registration_token = guard.read_token_from_header()
    user = guard.get_user_from_registration_token(registration_token)
    user.is_active = True
    db.session.commit()
    ret = {'access_token': guard.encode_jwt_token(user)}
    return jsonify(ret), 200


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

from flask import Flask, render_template, url_for, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from io import BytesIO

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
DATABASE = '/var/www/html/flaskapp/database.db'
app.config['DATABASE'] = DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'cs6065'
app.config['UPLOAD_FOLDER'] = 'uploads'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    text = db.Column(db.String(1000), nullable=True)
    wcount = db.Column(db.Integer(), nullable=True)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], 
                           render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "Password"})
    
    firstname = StringField(validators=[InputRequired(), Length(max=40)], 
                           render_kw={"placeholder": "First Name"})
    
    lastname = StringField(validators=[InputRequired(), Length(max=40)], 
                           render_kw={"placeholder": "Last Name"})
    
    email = StringField(validators=[InputRequired(), Length(max=40)], 
                           render_kw={"placeholder": "Email"})
    
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        
        if existing_user_username:
            raise ValidationError(
                "That username already exists."
            )
        

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(
            email=email.data).first()
        
        if existing_user_email:
            raise ValidationError(
                "That email already exists."
            )
        

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], 
                           render_kw={"placeholder": "Username"})
    
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")


class UploadForm(FlaskForm):
    upload = FileField(validators=[
        FileRequired(),
        FileAllowed(['txt'], 'Texts only!')
    ], render_kw={"placeholder": "File upload"})

    submit = SubmitField("Upload")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    log_form = LoginForm()
    if log_form.validate_on_submit():
        user = User.query.filter_by(username=log_form.username.data).first()
        if user: 
            if bcrypt.check_password_hash(user.password, log_form.password.data):
                login_user(user)
                return redirect(url_for('show_information', username=user.username))
            
    return render_template('find_info.html', form=log_form)


@app.route('/dashboard/<username>', methods=['GET', 'POST'])
@login_required
def dashboard(username):
    current_user = User.query.order_by(User.id.desc()).first()
    return render_template('dashboard.html', user=current_user)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/display', methods=['GET', 'POST'])
def display():
    current_user = User.query.order_by(User.id.desc()).first()
    return render_template('display.html', user=current_user)


@app.route('/show_information/<username>', methods=['GET', 'POST'])
def show_information(username):
    user = User.query.filter_by(username=username).first()
    return render_template('display.html', user=user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()

    if reg_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(reg_form.password.data)
        new_user = User(username=reg_form.username.data, password=hashed_password,
                        firstname=reg_form.firstname.data, lastname=reg_form.lastname.data,
                        email=reg_form.email.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('display'))

    return render_template('register.html', form=reg_form)


@app.route('/upload/<username>', methods=['GET', 'POST'])
def upload(username):
    upload_form = UploadForm()
    user = User.query.filter_by(username=username).first()

    if upload_form.validate_on_submit():
        file = upload_form.upload.data

        # Update the text field in the User instance
        user.text = file.stream.read().decode("utf-8")
        user.wcount = len(user.text.split())
        db.session.commit()
        
    return render_template('upload.html', form=upload_form, user=user)


@app.route('/download/<username>', methods=['GET'])
def download(username):
    user = User.query.filter_by(username=username).first()

    if user and user.text:
        filename = f"{user.username}_download.txt"
        download_content = f"{user.text}\nWord Count: {user.wcount}"
        bytes_object = bytes(download_content, encoding="utf-8")
        return send_file(BytesIO(bytes_object), 
                     download_name=filename, as_attachment=True)
    else:
        return "User or text content not found."


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

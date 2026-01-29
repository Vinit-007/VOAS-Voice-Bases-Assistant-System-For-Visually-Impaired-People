from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from flask_wtf.csrf import CSRFProtect

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Login', render_kw={"class": "btn btn-primary"})

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"class": "form-control"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)], render_kw={"class": "form-control"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    submit = SubmitField('Register', render_kw={"class": "btn btn-success"})

class MedicalForm(FlaskForm):
    uname = StringField('Name', validators=[DataRequired()], render_kw={"class": "form-control"})
    address = TextAreaField('Address', validators=[Optional()], render_kw={"class": "form-control"})
    allergies = TextAreaField('Allergies', validators=[Optional()], render_kw={"class": "form-control"})
    visionstatus = TextAreaField('Vision Status', validators=[Optional()], render_kw={"class": "form-control"})
    medications = TextAreaField('Medications', validators=[Optional()], render_kw={"class": "form-control"})
    surgeries = TextAreaField('Surgeries', validators=[Optional()], render_kw={"class": "form-control"})
    bloodgroup = SelectField('Blood Group', choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], validators=[Optional()], render_kw={"class": "form-control"})
    age = StringField('Age', validators=[Optional()], render_kw={"class": "form-control"})
    chronic_conditions = TextAreaField('Chronic Conditions', validators=[Optional()], render_kw={"class": "form-control"})
    emergency_contact = StringField('Emergency Contact', validators=[Optional()], render_kw={"class": "form-control"})
    blood_pressure = StringField('Blood Pressure', validators=[Optional()], render_kw={"class": "form-control"})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})

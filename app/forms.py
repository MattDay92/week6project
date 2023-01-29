from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class UserCreationForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField()

class loginform(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField()

class ItemSubmitForm(FlaskForm):
    name = StringField("Name", validators = [DataRequired()])
    img_url = StringField("Img_url", validators=[DataRequired()])
    details = StringField("Details", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    submit = SubmitField()
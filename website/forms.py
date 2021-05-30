from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo



class RegisterStudentForm(FlaskForm):
    """
    Form to register an user, will only be allowed to use by the admin of the page.
    """
    username = StringField('Username',
                        validators=[DataRequired(), Length(min=2, max=200)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password1 = PasswordField('Password',
                        validators=[DataRequired()])
    password2 = PasswordField('Repeat password',
                        validators=[DataRequired(), EqualTo(password1)])
    name = StringField('Complete Name',
                        validators=[DataRequired(), Length(min=2, max=200)])
    other_info = StringField('Other information',
                        validators=[Length(min=2, max=2000)])
    submit = SubmitField('Create Student')

class LoginForm(FlaskForm):
    """
    Login form, ti login the different users to the students page.
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=2, max=20)])
    password = PasswordField('Password',
                        validators=[DataRequired()])
    submit = SubmitField('Login')


class AddYogaPost(FlaskForm):
    """
    This form is to add a post in to the yoga blog, only allowed to use by the administrator of the page
    """
    title = StringField('Set the title of the post, (Titulo del articulo de yoga)',
                        validators=[DataRequired(), Length(min=2, max=1000)])
    main_content = TextAreaField('Here the main content of the post(contenido principal)',
                        validators=[DataRequired(), Length(min=2, max=200000)])
    secondary_content = TextAreaField('Here the secondary content (& = enter) (contenido secundario)',
                        validators=[DataRequired(), Length(min=2, max=200000)])
    web_picture = StringField('Add a picture url. (Cargar la imagen desde la web)',
                        validators=[Length(min=2, max=1000000)])
    submit = SubmitField('Add Post (Crear Post)')



class AddRecipe(FlaskForm):
    """
    This form is to add a post in to the recipies blog, only allowed to use by the administrator of the page
    """
    title = StringField('Set the title of the recipie, (Titulo de la receta)',
                        validators=[DataRequired(), Length(min=2, max=1000)])
    ingredients = TextAreaField('Here to put all the ingredients of the recipie (& = enter)(Seccion ingredientes)',
                        validators=[DataRequired(), Length(min=2, max=200000)])
    preparation = TextAreaField('Here the preparation of the recipie (& = enter) (Seccion preparacion de la receta)',
                        validators=[DataRequired(), Length(min=2, max=200000)])
    extra = TextAreaField('Any extra information needed to post (& = enter)  (Informacion complementaria)',
                        validators=[Length(min=2, max=200000)])
    web_picture = StringField('Add a picture url. (Cargar la imagen desde la web)',
                        validators=[Length(min=2, max=1000000)])
    category1 = StringField('First category')
    category2 = StringField('SECOND category')
    category3 = StringField('Third category')
    submit = SubmitField('Add recipie, (Crear receta)')

class LeaveYourEmailForm(FlaskForm):
    """
    This form is made to make the user of the page leave the email adrees to the admin of the page to receive the newsletter.
    """
    email = StringField('Leave your email to receive your first class.',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Suscribe')


class AddCourse(FlaskForm):
    """
    This form is to add a course in to the courses page. only allowed to use by the admin of the page 
    name: name of the course 
    type_of_course = define if the course is weekly, monthly or for the year.
    """
    name = StringField('Name of the course (Nombre del curso)',
                        validators=[DataRequired(), Length(min=2, max=200000)])
    type_of_course = StringField('Type of course (Tipo de curso)',
                        validators=[DataRequired(), Length(min=2, max=200000)])
    price = StringField('Price of the course (Precio)',
                        validators=[DataRequired(), Length(min=2, max=20000)])
    description = TextAreaField('ADD A DESCRIPTION FOR THE COURSE (& = enter) (Descripcion del curso)',
                        validators=[DataRequired(), Length(min=2, max=20000)])
    submit = SubmitField('Create Course, (Anadir curso)')


class LeaveYourMessageForm(FlaskForm):
    """
    This form is to leave a message to the admin of the page.
    Name : name of the user leaving a message
    Content: content of the message
    """
    name = StringField('Name',
                        validators=[DataRequired(), Length(min=2, max=200)])
    content = TextAreaField('Leave your message:',
                        validators=[DataRequired(), Length(min=2, max=20000)])
    submit = SubmitField('Send Message')
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField, FileField
from wtforms.validators import DataRequired, Email, ValidationError
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.widgets import TextArea
from app import mysql
from flask import session


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_username(form , field):

        cursor = mysql.connection.cursor()
        query = f"SELECT username FROM user WHERE username='{field.data}'"
        cursor.execute(query)
        data = cursor.fetchall()
        if( not data ):
            raise ValidationError("username not valid")
        cursor.close()
    
    def validate_password(form , field ):
        
        cursor = mysql.connection.cursor()
        uname = form.username.data
        query = f"SELECT password FROM user WHERE username='{uname}'"
        cursor.execute(query)
        data = cursor.fetchall()
        if( not data ):
            raise ValidationError("Something went wrong, contact admin")

        enteredPass = data[0]['password']
        if(enteredPass != field.data):
            raise ValidationError("Wrong password")
        cursor.close()
        
        

        


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name')
    email = EmailField('email' , validators=[DataRequired()])
    register = SubmitField('Register')


    def validate_username(form , field):
        cursor = mysql.connection.cursor()
        query = f"SELECT username FROM user WHERE username='{field.data}'"
        cursor.execute(query)
        data = cursor.fetchall()
        if( data ):
            raise ValidationError("Username already taken")
        cursor.close()
    
    def validate_email(form , field):
        cursor = mysql.connection.cursor()
        query = f"SELECT username FROM user WHERE email='{field.data}'"
        cursor.execute(query)
        data = cursor.fetchall()
        if( data ):
            raise ValidationError("email already taken by another user")
        cursor.close()

def generate_upload_book_form():

    cursor = mysql.connection.cursor()

    #Populate author choices option
    query = "SELECT aid , aname FROM author"
    cursor.execute(query)
    data = cursor.fetchall()
    choices=[]
    for dic in data:
        choices.append( ( dic['aid'] , dic['aname'] ) )
    authorChoices=choices

    #populate genre choices option
    query = "SELECT gid , gname FROM genre"
    cursor.execute(query)
    data = cursor.fetchall()
    choices=[]
    for dic in data:
        choices.append( ( dic['gid'] , dic['gname'] ) )
    genreChoices=choices

    class UploadBookForm(FlaskForm):
        bookTitle = StringField('Book Title' , validators = [DataRequired()])
        bookCover = FileField('Book Cover Photo' , validators=[FileRequired() , FileAllowed(['jpg' , 'jpeg'])])
        bookAuthor = SelectField('Book Author' , coerce=int , choices=authorChoices)
        bookGenre = SelectField( 'Genre' , coerce=int, choices=genreChoices)
        submitBook = SubmitField('Submit')

    return UploadBookForm() 



class UploadAuthorForm(FlaskForm):
    authorName = StringField('Author Name' , validators=[DataRequired()])
    submitAuthor = SubmitField('Submit')

class UploadGenreForm(FlaskForm):
    genreName = StringField('Genre Name' , validators=[DataRequired()])
    submitGenre = SubmitField('Submit')

    def validate_genreName(form , field):
        cursor = mysql.connection.cursor()
        query = f"SELECT gname FROM genre WHERE gname='{field.data}'"
        cursor.execute(query)
        data = cursor.fetchall()
        if( data ):
            raise ValidationError("Genre name already taken")
        cursor.close()

def generate_review_form():

    cursor = mysql.connection.cursor()
    query = "SELECT bid , btitle FROM book"
    cursor.execute(query)
    data = cursor.fetchall()
    choices=[]
    for dic in data:
        choices.append( ( dic['bid'] , dic['btitle'] ) )
    bookChoices=choices

    class ReviewForm(FlaskForm):

        bookTitle = SelectField('Book Title', coerce=int, choices=bookChoices)
        reviewText = StringField('ReviewText' , widget= TextArea() , validators=[DataRequired()]) 
        recommend = BooleanField('Recommend' , render_kw={'checked': True})
        submit = SubmitField('Submit')
        
        def validate_bookTitle(form , field):
            
            query = f"SELECT * from review WHERE uid={session['uid']} AND bid={field.data}"
            cursor.execute(query)
            data = cursor.fetchall()
            if(data):
                raise ValidationError("You have already submitted a review of this book !")
            cursor.close()



    
    return ReviewForm()
    # def validate_reviewText(form, field):
    #         cursor = mysql.connection.cursor()
    #         query = f"SELECT reviewText FROM book WHERE bookTitle='{field.data}'"
    #         cursor.execute(query)
    #         data = cursor.fetchall()
    #         if( not data ):
    #                 raise ValidationError("No reviews available yet")
    #                 cursor.close()

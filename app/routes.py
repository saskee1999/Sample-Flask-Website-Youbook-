from flask import render_template, flash, redirect, url_for, jsonify, session, request
from app import app, mysql
from app.forms import LoginForm, RegisterForm, UploadAuthorForm, UploadGenreForm, generate_upload_book_form, generate_review_form
from wtforms import SelectField
from pprint import pprint
import json
from werkzeug.utils import secure_filename
from datetime import datetime
import re

@app.route('/')
@app.route('/index')
def index():

    #setup
    cursor = mysql.connection.cursor()

    #fetch toprated

    query = "SELECT * from book ORDER BY arating DESC LIMIT 9"
    cursor.execute(query)
    toprated = cursor.fetchall()

    #fetch all genres
    query = "SELECT * from genre"
    cursor.execute(query)
    genres = cursor.fetchall()
    
    #fecth all books in respective geres
    for genre in genres:
        gid = genre['gid']
        gname = genre['gname']
        genre['books'] = []
        query = f"SELECT * from book WHERE gid={gid}"
        cursor.execute(query)
        genre['books'] = cursor.fetchall()
    
    
    
    #latest

    query = "SELECT review.uid as `rid` , review.bid as `bid` , review.content as `content` , \
        review.dt as `dt` , review.rec as `rec` , user.username as `username` , book.aid as `aid` , \
        author.aname as `aname` , book.btitle as `btitle` from review, user, book, author where user.uid = review.uid \
        and review.bid=book.bid and book.aid=author.aid order by review.dt desc limit 3"
    cursor.execute(query)
    latest = cursor.fetchall()

    #allr
    query = "SELECT review.uid as `rid` , review.bid as `bid` , \
        review.content as `content` , review.dt as `dt` , review.rec \
        as `rec` , user.username as `username` , book.aid as `aid` , author.aname as `aname` ,\
        book.btitle as `btitle` from review, user, book, author where user.uid = review.uid \
        and review.bid=book.bid and book.aid=author.aid"
    cursor.execute(query)
    allr = cursor.fetchall()
    

    #check for user
    user=""
    is_admin=""
    uid=""
    try:
        user = session['user']
        uid = session['uid']
        is_admin = session['is_admin']
    except KeyError:
        pass
    

    return render_template('index.html', title='Home', user=user, is_admin=is_admin , genres = genres , latest=latest , allr = allr, toprated=toprated)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # flash('Login requested for user {}, remember_me={}'.format(
        #     form.username.data, form.remember_me.data))

        session['user'] = form.username.data
        usr = session['user']
        cursor = mysql.connection.cursor()
        query = f"SELECT uid , is_admin FROM user WHERE username='{usr}'"
        cursor.execute(query)
        data = cursor.fetchall()[0]
        session['uid'] = data['uid']
        session['is_admin'] = data['is_admin']

        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)

@app.route('/logout' , methods=['GET' , 'POST'])
def logout():
    session['user'] = None
    session['uid'] = None
    session['is_admin'] = None
    flash("Logout successful" , "success")
    return redirect(url_for('login'))


@app.route('/register' , methods=['GET' , 'POST'])
def register():
   
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data
        email = str(form.email.data)
        query = f"INSERT INTO user(username , password , name , email) values('{username}' , '{password}' , '{name}' , '{email}')"
        print(query)
        
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        mysql.connection.commit()
        cursor.close()
        flash("Registration Successful" , "success")
        return redirect('login')



    return render_template('register.html'  , form = form)


@app.route('/uploadBook' , methods=['GET' , 'POST'])
def uploadBook():

    try:
        ia = session['is_admin']
    except KeyError:
        flash("You must be admin to upload book" , "error")
        return redirect(url_for('index'))
        pass
    
    if(not session['is_admin']):
        flash("You must be admin to upload book" , "error")
        return redirect(url_for('index'))
    


    bookForm = generate_upload_book_form()
    authorForm = UploadAuthorForm()
    genreForm = UploadGenreForm()
    cursor = mysql.connection.cursor()


    if bookForm.submitBook.data and bookForm.validate_on_submit():

        aid = bookForm.bookAuthor.data
        gid = bookForm.bookGenre.data
        btitle = bookForm.bookTitle.data
        query = f"INSERT INTO book(aid , gid , btitle) values({aid} , {gid} , '{btitle}')"
        cursor.execute(query)
        mysql.connection.commit()
        query = "SELECT last_insert_id() as `bid`"
        cursor.execute(query)
        bid = cursor.fetchall()[0]['bid']
        photo = bookForm.bookCover.data
        coverPath = "app/static/images/tbooks/" + str(bid) + ".jpg"
        photo.save(coverPath)
        

    if authorForm.submitAuthor.data and authorForm.validate_on_submit():
        
        query = f"INSERT INTO author(aname) VALUES('{authorForm.authorName.data}')"
        cursor.execute(query)
        mysql.connection.commit()
        flash("Author successfull added", "success")
        return redirect(url_for('uploadBook'))


    if genreForm.submitGenre.data and genreForm.validate_on_submit():
        query = f"INSERT INTO genre(gname) VALUES('{genreForm.genreName.data}')"
        cursor.execute(query)
        mysql.connection.commit()

        flash("Genre successfully added" , "success")
        return redirect(url_for('uploadBook'))

    return render_template('uploadBook.html' , bookForm=bookForm , authorForm = authorForm , genreForm = genreForm)

@app.route('/review' , methods=['GET' , 'POST'])
def review():
   
    form = generate_review_form()
    cursor = mysql.connection.cursor()

    if form.validate_on_submit():

        text = form.reviewText.data
        text = re.escape(text)
        bid = form.bookTitle.data
        rec = form.recommend.data
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uid = session['uid']

        if rec : rec=1
        else : rec = 0

        query = f"INSERT INTO review(bid , content , rec , dt, uid) VALUES({bid} , '{text}' , {rec} , '{dt}' , {uid})"
        
        cursor.execute(query)
        mysql.connection.commit()


        #update avg rating

        query = f"SELECT count(*) as `cnt` from review where bid={bid}"
        cursor.execute(query)
        totalReviews = cursor.fetchall()[0]['cnt']

        query = f"SELECT count(*) as `cnt` from review where bid={bid} and rec=1"
        cursor.execute(query)
        totalPos = cursor.fetchall()[0]['cnt']

        newrate = ((totalPos+1)/(totalReviews+2) )*100

        query = f"UPDATE book SET arating={ newrate } WHERE bid={bid}"
        cursor.execute(query)
        mysql.connection.commit()



        flash("Review successfully added" , "success")
        return redirect(url_for('review'))
        
        
        

    return render_template('review.html' , form = form )

@app.route('/ajax' , methods=['POST' , 'GET'])
def ajax():
    return jsonify({'data': 'successful'})


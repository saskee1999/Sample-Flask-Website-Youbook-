# from app import db
from app import app
# class User(db.Model):
#     User_ID = db.Column(db.Integer, primary_key=True)
#     Username = db.Column(db.String(64), index=True, unique=True)
#     password = db.Column(db.String(128))

#     def __repr__(self):
#         return '<User {}>'.format(self.Username)

# class Author(db.Model):
#     Author_ID = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(128), unique=True)

#     def __repr__(self):
#         return '<Author {}>'.format(self.Author_ID)

# class Book(db.Model):
# 	Book_ID = db.Column(db.Integer, primary_key=True)
# 	BookName = db.Column(db.String(30))
# 	Rating = db.Column(db.Integer)
# 	Author_ID = db.Column(db.Integer, db.ForeignKey('Author_ID'))

# 	def __repr__(self):
# 		return '<Book {}>'.format(self.BookName)

# class Reviews(db.Model):
# 	Book_ID = db.Column(db.Integer, db.ForeignKey('Book_ID'))
# 	User_Reviews = db.Column(db.String(180))
# 	Review_ID = db.Column(db.Integer, primary_key=True)

# 	def __repr__(self):
# 		return'<Reviews {}>'.format(self.Book_ID)
# class Genre:
#  	Book_ID = db.Column(db.Integer, db.ForeignKey('Book_ID'))
#  	g_name = db.Column(db.String(30))

#  	def __repr__(self):
#  		return'<Genre {}>'.format(self.g_name)

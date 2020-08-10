# from pprint import pprint
# from app import app, db
# from app.models import *

# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'User': User, 'Author': Author, 'Book': Book, 'Reviews': Reviews, 'Genre': Genre}
from app import app
if __name__ == "__main__":
    app.run()


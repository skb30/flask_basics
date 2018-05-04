from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)


# setup the enviroment variables for the projcet
app.config.update(
    # used by flask to secure data in cookies
    SECRET_KEY='topsecret',

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:hje000sb@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFCATIONS=False

)

# creates a link/bind to the database
db = SQLAlchemy(app)

# create the model for Object Resource Mapping(ORM)
class Publication(db.Model): # inherit the Model class
    __tablename_ = 'publication' # name of the table

    # use ORM to create the SQL
    pub_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False) # can't be null

    def __init__(self, name): # class constructor

        self.name = name

    # this built-in creates a string version of the instance which
    # helps in producing a readable format of the output.
    # by using this built-in, you can create an instance
    # of Publication then execute that instance to get the
    # output string. e,g pub=Publication(11,'Oxford Publications')
    def __repr__(self):
        # create 2 place holders, name and id
        return 'Name is {} '.format(self.name)

class Book(db.Model):

    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # Relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.pub_id'))

    def __init__(self, title, author, avg_rating, format, image, num_pages, \
                pub_id): # class constructor
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)


# example of 2 routes calling the same function
@app.route('/index')
@app.route('/')
def hello_flask():
    return '<h1>Hello flask</h1>'

@app.route('/new/')
def query_strings(greeting="hello"):
    # if user doesn't supply a value the default will be hello
    query_val = request.args.get('greeting', greeting)
    return '<h1> the greeting is : {}'.format(query_val)

@app.route('/user')
# route with a parm
@app.route('/user/<name>')
def no_query_string(name='mina'):
    return '<h1> hello there: {} </h1>'.format(name)

@app.route('/macros')
def jinja_macros():
    movies = {'autopsy': 02.14,
              'rain man': 1.45,
              'gone with the wind': 3.30,
              'child 44': 2.15}
    return render_template('using_macros.html', movies=movies, name='Scott')
@app.route('/table')
def movies():
    movies = {'autopsy': 02.14,
              'rain man': 1.45,
              'gone with the wind': 3.30,
              'child 44': 2.15}
    return render_template('table_data.html', movies=movies, name='Scott')
@app.route('/filters')
def filter_data():

    movies = {'autopsy': 02.14,
      'rain man': 1.45,
      'gone with the wind': 3.30,
      'child 44': 2.15}

    return render_template('filter_data.html',
                            movies=movies, name=None,
                            film='a christmas carol')
# run the code inline instead of importing
if __name__ == '__main__':

    # creates tables if they don't exsist
    db.create_all()
    app.run(debug=True)

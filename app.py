
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import chatbot

import pymysql
pymysql.install_as_MySQLdb()

from dotenv import load_dotenv
load_dotenv()  # Load environment variables

import os
import pymysql
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Time

pymysql.install_as_MySQLdb()

# Now you can use os.environ.get('VARIABLE_NAME') to access your environment variables
api_key = os.environ.get('GOOGLE_MAPS_API_KEY')

app = Flask(__name__)

app.secret_key = '1243'  # Set a secret key for session management

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Capstoneproject123@34.102.79.31/daycare_db'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Users(db.Model):
    __tablename__ = 'users'  # Explicitly specify the table name
    UserID = db.Column(db.Integer, primary_key=True)
    UserRole = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    daycare_owner = db.relationship('DaycareOwner', backref='users', uselist=False)
    parent = db.relationship('Parent', backref='users', uselist=False)
    volunteer = db.relationship('Volunteer', backref='users', uselist=False)


class DaycareOwner(db.Model):
    OwnerID = db.Column(db.Integer, db.ForeignKey('users.UserID'), primary_key=True)
    OwnerName = db.Column(db.String(255), nullable=False)
    Capacity = db.Column(db.Integer)
    LicenseNumber = db.Column(db.String(100))
    FromTime = db.Column(db.Time)
    ToTime = db.Column(db.Time)
    Phone = db.Column(db.String(50))
    Street = db.Column(db.String(255))
    City = db.Column(db.String(100))
    State = db.Column(db.String(50))
    Zip = db.Column(db.String(10))
    SpecialNeeds = db.Column(db.String(10))
    Website = db.Column(db.String(255))

class Parent(db.Model):
    ParentID = db.Column(db.Integer, db.ForeignKey('users.UserID'), primary_key=True)
    ParentName = db.Column(db.String(255), nullable=False)
    NumberOfChildren = db.Column(db.Integer)
    ChildrenAges = db.Column(db.String(255))

class Volunteer(db.Model):
    VolunteerID = db.Column(db.Integer, db.ForeignKey('users.UserID'), primary_key=True)
    FullName = db.Column(db.String(255), nullable=False)
    SSN = db.Column(db.String(50))  # Consider security implications
    Age = db.Column(db.Integer)
    HoursAvailable = db.Column(db.String(50))

class Age(db.Model):
    AgeID = db.Column(db.Integer, primary_key=True)
    AgeGroup = db.Column(db.String(50), nullable=False)

class Daycare_AgesServed(db.Model):
    OwnerID = db.Column(db.Integer, db.ForeignKey('daycare_owner.OwnerID'), primary_key=True)
    AgeID = db.Column(db.Integer, db.ForeignKey('age.AgeID'), primary_key=True)

class Day(db.Model):
    DayID = db.Column(db.Integer, primary_key=True)
    DayName = db.Column(db.String(50), nullable=False)

class Daycare_DaysOfOperation(db.Model):
    OwnerID = db.Column(db.Integer, db.ForeignKey('daycare_owner.OwnerID'), primary_key=True)
    DayID = db.Column(db.Integer, db.ForeignKey('day.DayID'), primary_key=True)

class Volunteer_DaysAvailable(db.Model):
    VolunteerID = db.Column(db.Integer, db.ForeignKey('volunteer.VolunteerID'), primary_key=True)
    DayID = db.Column(db.Integer, db.ForeignKey('day.DayID'), primary_key=True)

class ContactForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)

class Daycare(db.Model):
    __tablename__ = 'daycare_profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(255))
    website = db.Column(db.String(255))
    security_features = db.Column(db.Text)
    safety_protocols = db.Column(db.Text)
    license_number = db.Column(db.String(100))
    accreditations = db.Column(db.Text)
    testimonials = db.Column(db.Text)
    average_ratings = db.Column(db.DECIMAL(3, 2))
    zip_code = db.Column(db.String(10))
    operating_days = db.Column(db.String(255))
    opening_time = db.Column(Time)
    closing_time = db.Column(Time)
    min_age = db.Column(db.Integer)
    max_age = db.Column(db.Integer)
    max_children = db.Column(db.Integer)
    meals = db.Column(db.Text)
    educational_programs = db.Column(db.Text)
    extracurricular_activities = db.Column(db.Text)
    image_url = db.Column(db.String(255)) 
    latitude = db.Column(db.Float)  
    longitude = db.Column(db.Float)  
  


    def __repr__(self):
        return f"Daycare(name='{self.name}', zip_code='{self.zip_code}')"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/index")
def index():
    return render_template("index.html")  

@app.route("/signin")
def signin():
    return render_template("signin.html")



@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/blog1")
def blog1():
    return render_template("blog1.html")

@app.route("/blog2")
def blog2():
    return render_template("blog2.html")

@app.route("/blog3")
def blog3():
    return render_template("blog3.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    success = False
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        new_contact = ContactForm(name=name, email=email, subject=subject, message=message)
        db.session.add(new_contact)
        db.session.commit()
        
        success = True
    
    return render_template('contact.html', success=success)

@app.route('/success')
def success():
    return 'Success!'

@app.route("/daycareowners")
def daycareowners():
    return render_template("daycareowners.html")

@app.route("/daycares")
def daycares():
    return render_template("daycares.html")

@app.route("/parent")
def parent():
    return render_template("parent.html")

@app.route("/results")
def results():
    daycares = Daycare.query.all()
    return render_template("results.html", daycares=daycares)

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/services1")
def services1():
    return render_template("services1.html")

@app.route("/volunteer")
def volunteer():
    return render_template("volunteer.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        zip_code = request.form['zip']
        # Change the filter from zip to zip_code
        daycares = Daycare.query.filter_by(zip_code=zip_code).all()
        return render_template('results.html', daycares=daycares)
    else:
        # Handle the GET request, possibly returning a search form
        return render_template('search_form.html')


@app.route('/daycare/<int:daycare_id>')
def daycare_profiles(daycare_id):
    daycare = Daycare.query.get_or_404(daycare_id)
    return render_template('profile.html', daycare=daycare, api_key=api_key)


# Chatbot routes
# from chatbot import create_assistant
assistant_id = "asst_cj0ojW3O4BwUmDYyYCDfBlfy"  


@app.route('/get_chatbot_response', methods=['POST'])
def get_chatbot_response():
    user_message = request.json.get('message')
    chatbot_response = chatbot.get_response(user_message, assistant_id)
    return jsonify({'response': chatbot_response})


if __name__ == "__main__":
    with app.app_context():
        pass
        db.create_all()
    app.run(debug=True)

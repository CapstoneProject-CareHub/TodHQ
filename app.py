from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Snowwhite16.@localhost/daycare_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    UserRole = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    daycare_owner = db.relationship('DaycareOwner', backref='user', uselist=False)
    parent = db.relationship('Parent', backref='user', uselist=False)
    volunteer = db.relationship('Volunteer', backref='user', uselist=False)

class DaycareOwner(db.Model):
    OwnerID = db.Column(db.Integer, db.ForeignKey('user.UserID'), primary_key=True)
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
    ParentID = db.Column(db.Integer, db.ForeignKey('user.UserID'), primary_key=True)
    ParentName = db.Column(db.String(255), nullable=False)
    NumberOfChildren = db.Column(db.Integer)
    ChildrenAges = db.Column(db.String(255))

class Volunteer(db.Model):
    VolunteerID = db.Column(db.Integer, db.ForeignKey('user.UserID'), primary_key=True)
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
    __tablename__ = 'daycares'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    zip = db.Column(db.String(10), nullable=False)
    rating = db.Column(db.String(5), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return f"Daycare('{self.name}', '{self.zip}')"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/about")
def about():
    return render_template("about.html")

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
    return render_template("results.html")

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
        print(f"ZIP Code: {zip_code}")  # Check the received ZIP code
        daycares = Daycare.query.filter_by(zip=zip_code).all()
        print(f"Daycares: {daycares}")  # Check the retrieved daycares
        return render_template('results.html', daycares=daycares)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import chatbot
import bcrypt

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

# class Users(db.Model):
    
#     UserID = db.Column(db.Integer, primary_key=True)
#     UserRole = db.Column(db.String(50), nullable=False)
#     Email = db.Column(db.String(255), unique=True, nullable=False)
#     Password = db.Column(db.String(255), nullable=False)
#     daycare_owner = db.relationship('DaycareOwner', backref='users', uselist=False)
#     parent = db.relationship('Parent', backref='users', uselist=False)
#     volunteer = db.relationship('Volunteer', backref='users', uselist=False)

class User(db.Model):
    __tablename__ = 'User'  # Explicitly specify the table name
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(50))
    Password = db.Column(db.String(255), nullable=False)
    State = db.Column(db.String(255))  # New field
    City = db.Column(db.String(255))   # New field
    zip_code = db.Column(db.String(20)) # New field
    Role = db.Column(db.String(20), nullable=False)
    Experience = db.Column(db.Integer, nullable=False)
    Reference = db.Column(db.Text, nullable=False)
    AvailableDays = db.Column(db.String(255), nullable=False)  # From Volunteer model
    AvailableTimings = db.Column(db.String(255))  # From Volunteer model
    IDProofPath = db.Column(db.String(255), nullable=False)

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


class contact_form(db.Model):
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

# # New route to handle sign-in form submission
@app.route("/signin", methods=['POST'])
def signin_post():
    email = request.form['email']
    password = request.form['password']

    # Find user by email
    user = User.query.filter_by(Email=email).first()

    # Check if user exists and the password is correct
    if user and bcrypt.checkpw(password.encode('utf-8'), user.Password.encode('utf-8')):
        # User is authenticated, create a session
        session['user_id'] = user.UserID
        success = f"You have successfully logged in, {user.FirstName}!"
        # return redirect(url_for('index.html'))  # Redirect to a dashboard or another page
        return render_template("index.html", success=success)
    else:
        # Authentication failed
        error = "Invalid Username or Password, Please try again."
        return render_template("signin.html", error=error)
        

# Example route for a user dashboard (you need to create this)
@app.route("/dashboard")
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            return render_template("dashboard.html", user=user)
        else:
            # Handle case where user is not found
            return "User not found", 404
    else:
        return redirect(url_for('signin'))
# Route for logout
@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

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
        
        new_contact = contact_form(name=name, email=email, subject=subject, message=message)
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

@app.route('/submit_volunteer', methods=['POST'])
def submit_volunteer():
    # Extract data from the form
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']
    state = request.form['state']
    city = request.form['city']
    zip_code = request.form['zip_code']
    phone = request.form['phone']
    available_timings = ', '.join(request.form.getlist('availableHours[]'))
    experience = request.form['experience']
    reference = request.form['reference']
    available_days = ', '.join(request.form.getlist('availableDays[]'))


    # Save the file to a specific folder
    upload_folder = 'docs/uploaded_files'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    id_proof_file = request.files['idProof']
    id_proof_path = os.path.join(upload_folder, id_proof_file.filename)
    id_proof_file.save(id_proof_path)

    # Hash the password
    password = request.form['password'].encode('utf-8')  # Convert the password to bytes
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    # Create a new User instance
    new_user = User(
        FirstName=first_name,
        LastName=last_name,
        Email=email,
        Password=hashed_password.decode('utf-8'),
        State=state,
        City=city,
        zip_code=zip_code,
        phone=phone,
        Role=role,
        Experience=experience,
        Reference=reference,
        AvailableDays=available_days,
        AvailableTimings=available_timings,
        IDProofPath=id_proof_path
    )

    db.session.add(new_user)
    db.session.commit()

    # Redirect or show a success message
    return render_template('volunteer.html', success=True)

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

@app.route('/volunteer_search', methods=['GET','POST'])
def volunteer_search():
    if request.method == 'POST':
        zip_code = request.form['zip_code']
        role = request.form['role']

        if role == 'volunteer':
            # Search logic for volunteers
            # Assuming Volunteer information is stored in User table
            results = User.query.filter(User.zip_code == zip_code, User.Role == 'volunteer').all()
            print("Results: ", results)  # Debugging line
            return render_template('volunteer_results.html', results=results)
        elif role == 'caregiver':
            # Search logic for caregivers
            results = User.query.filter(User.zip_code == zip_code, User.Role == 'caregiver').all()
            print("Results: ", results)  # Debugging line
            return render_template('volunteer_results.html', results=results)
        else:
            # Default search logic for daycare providers
            results = Daycare.query.filter_by(zip_code=zip_code).all()
            return render_template('results.html', daycares=daycares)
    return render_template('volunteer_search_form.html')

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

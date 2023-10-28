from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/success')
def success():
    return 'Signup successful!'

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
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contact_form (name, email, subject, message) VALUES (%s, %s, %s, %s)", (name, email, subject, message))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('success'))
    
    return render_template('contact.html')

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

@app.route("/services")
def services1():
    return render_template("services1.html")

@app.route("/volunteer")
def volunteer():
    return render_template("volunteer.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/daycares.json")
def daycares_json():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'daycares.json')

if __name__ == "__main__":
    app.run(debug=True)

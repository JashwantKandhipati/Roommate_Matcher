from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configure a local SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roommates.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    
    # Quantifying Lifestyle Habits as integer percentages (0-100)
    noise_level = db.Column(db.Integer, nullable=False) 
    cleanliness = db.Column(db.Integer, nullable=False) 
    budget = db.Column(db.Integer, nullable=False)
    
    # We can add booleans or strings for Smoking/Drinking, Hobbies, etc. later

# Create the database tables
with app.app_context():
    db.create_all()

# Route for the homepage / UI
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
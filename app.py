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
    college = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    # We will add the other preference columns to this database table later!

# Create the database tables
with app.app_context():
    db.create_all()

# Route 1: The Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Grab the data from the form
        name = request.form.get('name')
        college = request.form.get('college')
        phone = request.form.get('phone')
        
        # Save the basic user info to the database
        new_user = User(name=name, college=college, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        
        # Redirect them to the preferences page, passing along their new user ID
        return redirect(url_for('preferences', user_id=new_user.id))
    
    # If it's just a GET request, show them the login page
    return render_template('login.html')

# Route 2: The Input Forms Page
@app.route('/preferences/<int:user_id>')
def preferences(user_id):
    return render_template('preferences.html', user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)
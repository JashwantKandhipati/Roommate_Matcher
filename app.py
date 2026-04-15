from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roommates.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# The updated User database model with ALL metrics
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    college = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    
    # Lifestyle Metrics
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    hobbies = db.Column(db.String(200), nullable=True)
    budget = db.Column(db.Integer, nullable=True)
    cleanliness = db.Column(db.Integer, nullable=True)
    noise_level = db.Column(db.Integer, nullable=True)
    sleep_schedule = db.Column(db.String(20), nullable=True)
    smoking = db.Column(db.Boolean, default=False)
    drinking = db.Column(db.Boolean, default=False)

def calculate_compatibility(user1, user2):
    """Calculates compatibility score on a 0-100 scale."""
    score = 0
    
    # Budget compatibility (within $200) - 30 points
    if abs((user1.budget or 0) - (user2.budget or 0)) <= 200:
        score += 30

    # Lifestyle compatibility (Cleanliness & Noise) - 40 points total
    # This logic accounts for the 0-100 slider values
    clean_diff = abs((user1.cleanliness or 0) - (user2.cleanliness or 0))
    noise_diff = abs((user1.noise_level or 0) - (user2.noise_level or 0))
    # We penalize the score based on how far apart the preferences are
    score += max(0, 40 - (clean_diff + noise_diff) // 4)

    # Habits match (Smoking & Drinking) - 20 points total
    if user1.smoking == user2.smoking:
        score += 10
    if user1.drinking == user2.drinking:
        score += 10

    # College match - 10 points
    if user1.college.lower() == user2.college.lower():
        score += 10
        
    return score

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        college = request.form.get('college')
        phone = request.form.get('phone')
        
        new_user = User(name=name, college=college, phone=phone)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('preferences', user_id=new_user.id))
    
    return render_template('login.html')

@app.route('/preferences/<int:user_id>', methods=['GET', 'POST'])
def preferences(user_id):
    user = User.query.get_or_404(user_id) # Find the user in the database
    
    if request.method == 'POST':
        # Update the user's empty columns with the form data
        user.age = request.form.get('age')
        user.gender = request.form.get('gender')
        user.hobbies = request.form.get('hobbies')
        user.budget = request.form.get('budget')
        user.cleanliness = request.form.get('cleanliness')
        user.noise_level = request.form.get('noise')
        user.sleep_schedule = request.form.get('sleep_schedule')
        user.smoking = True if request.form.get('smoking') else False
        user.drinking = True if request.form.get('drinking') else False
        
        db.session.commit() # Save the updates
        return redirect(url_for('matches', user_id=user.id)) # Send to matches page
        
    return render_template('preferences.html', user_id=user_id)

@app.route('/matches/<int:user_id>')
def matches(user_id):
    user = User.query.get_or_404(user_id)
    # Fetch everyone except the person currently logged in
    all_other_users = User.query.filter(User.id != user_id).all()
    
    # Calculate scores for each potential match
    scored_matches = []
    for other in all_other_users:
        score = calculate_compatibility(user, other)
        # Store both the user object and their score
        scored_matches.append({
            'data': other,
            'score': score
        })
        
    # Sort matches by highest score first
    scored_matches.sort(key=lambda x: x['score'], reverse=True)
    
    return render_template('matches.html', current_user=user, potential_matches=scored_matches)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roommates.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DATABASE MODEL
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
    smoking = db.Column(db.Boolean, default=False)
    drinking = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

# MATCHING ALGORITHM
def calculate_compatibility(user1, user2):
    score = 100.0
    
    # Cleanliness (30%)
    clean_diff = abs((user1.cleanliness or 50) - (user2.cleanliness or 50))
    score -= (clean_diff * 0.30)
    
    # Noise Level (30%)
    noise_diff = abs((user1.noise_level or 50) - (user2.noise_level or 50))
    score -= (noise_diff * 0.30)
    
    # Smoking Habit (20%)
    if user1.smoking != user2.smoking:
        score -= 20
        
    # Drinking Habit (10%)
    if user1.drinking != user2.drinking:
        score -= 10
        
    # Budget (10%)
    budget_diff = abs((user1.budget or 0) - (user2.budget or 0))
    budget_penalty = min((budget_diff / 500.0) * 10, 10)
    score -= budget_penalty
    
    return round(max(0, score))

# ROUTES

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
    user = User.query.get_or_404(user_id) 
    
    if request.method == 'POST':
        user.age = request.form.get('age')
        user.gender = request.form.get('gender')
        user.hobbies = request.form.get('hobbies')
        user.budget = request.form.get('budget')
        user.cleanliness = request.form.get('cleanliness')
        user.noise_level = request.form.get('noise')
        user.smoking = True if request.form.get('smoking') else False
        user.drinking = True if request.form.get('drinking') else False
        
        db.session.commit() 
        return redirect(url_for('matches', user_id=user.id)) 
        
    return render_template('preferences.html', user_id=user_id)


@app.route('/matches/<int:user_id>')
def matches(user_id):
    current_user = User.query.get_or_404(user_id)
    all_other_users = User.query.filter(User.id != user_id).all()
    
    matches_list = []
    for other_user in all_other_users:
        match_score = calculate_compatibility(current_user, other_user)
        matches_list.append({
            'user': other_user,
            'score': match_score
        })
        
    matches_list.sort(key=lambda x: x['score'], reverse=True)
    
    return render_template('matches.html', current_user=current_user, matches_list=matches_list)

if __name__ == '__main__':
    app.run(debug=True)
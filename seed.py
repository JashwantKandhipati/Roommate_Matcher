from app import app, db, User

def seed_data():
    with app.app_context():
        db.create_all()
        # Add your standard test users here
        user1 = User(name="Test1", college="CSUF", phone="123456", budget=1300, cleanliness=84)
        db.session.add(user1)
        db.session.commit()
        print("Database seeded!")

if __name__ == "__main__":
    seed_data()
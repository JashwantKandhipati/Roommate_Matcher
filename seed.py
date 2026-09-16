import random
from app import app, db, User

COLLEGES = [
    "UCLA", "UCSD", "UCR", "UCSB", "UCI",
    "CSUF", "CSULB", "CSULA", "CSUN", "CPP", "SDSU",
    "USC", "Pepperdine", "LMU", "Chapman"
]

FIRST_NAMES = [
    "Alex", "Jordan", "Taylor", "Morgan", "Sam", "Chris", "Pat", "Riley",
    "Casey", "Dakota", "Jamie", "Avery", "Ethan", "Liam", "Maya", "Chloe",
    "Noah", "Sophia", "Lucas", "Olivia", "Daniel", "Emma", "Aiden", "Ava"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Lee"
]

GENDERS = ["Male", "Female", "Non-binary", "Prefer not to say"]
SLEEP_SCHEDULES = ["Early Bird", "Night Owl", "Flexible"]
HOBBIES_LIST = ["Gym", "Gaming", "Reading", "Hiking", "Cooking", "Music", "Photography", "Coding", "Anime", "Art"]
BIOS = [
    "Looking for a quiet roommate who respects personal space and quiet hours.",
    "Outgoing student looking for someone who likes to hang out and explore campus!",
    "Pretty laid back, clean, and usually busy with classes during the week.",
    "Love cooking and hosting small study sessions on weekends.",
    "Very organized and clean freak looking for a like-minded housemate."
]

def seed_database(users_per_college=5):
    with app.app_context():
        # 1. Clear all existing data
        print("Wiping existing user records...")
        try:
            db.session.query(User).delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error clearing records: {e}")

        # 2. Reset the PostgreSQL auto-increment sequence to 1
        if db.engine.name == 'postgresql':
            try:
                db.session.execute(db.text("ALTER SEQUENCE user_id_seq RESTART WITH 1;"))
                db.session.commit()
                print("Primary key sequence reset to 1.")
            except Exception as e:
                db.session.rollback()

        # 3. Generate random user entries for each college
        print(f"Generating {users_per_college} random profiles for each college...")
        generated_users = []
        
        for college in COLLEGES:
            for _ in range(users_per_college):
                first = random.choice(FIRST_NAMES)
                last = random.choice(LAST_NAMES)
                name = f"{first} {last}"
                phone = f"{random.randint(200, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
                selected_hobbies = ", ".join(random.sample(HOBBIES_LIST, k=random.randint(2, 4)))
                
                user = User(
                    name=name,
                    college=college,
                    phone=phone,
                    year=random.randint(1, 4),
                    gender=random.choice(GENDERS),
                    hobbies=selected_hobbies,
                    budget=random.randrange(800, 2500, 50),
                    cleanliness=random.randint(1, 10),
                    noise_level=random.randint(1, 10),
                    sleep_schedule=random.choice(SLEEP_SCHEDULES),
                    smoking=random.choice([True, False]),
                    drinking=random.choice([True, False]),
                    bio=random.choice(BIOS)
                )
                generated_users.append(user)

        db.session.add_all(generated_users)
        
        try:
            db.session.commit()
            print(f"Successfully seeded {len(generated_users)} dummy profiles across {len(COLLEGES)} colleges!")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to commit seeded records: {e}")

if __name__ == "__main__":
    # Change users_per_college to control dataset size (e.g., 5 = 75 total users)
    seed_database(users_per_college=5)
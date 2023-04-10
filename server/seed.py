from random import choice as rc

from faker import Faker

from app import app
from models import db, Activity, Signup, Camper

fake = Faker()

def create_activities():
    pass

if __name__ == '__main__':

    with app.app_context():
        print("Clearing db...")
        Activity.query.delete()
        Signup.query.delete()
        Camper.query.delete()

        print("Seeding activities...")
        activities = create_activities()

        print("Done seeding!")

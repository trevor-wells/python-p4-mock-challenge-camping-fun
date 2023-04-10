import json
from os import environ
from flask import request

from app import app
from models import db, Activity, Signup, Camper

class TestApp:
    '''Flask application in app.py'''

    def test_gets_campers(self):
        '''retrieves campers with GET requests to /campers.'''

        with app.app_context():
            clark = Camper(name="Clark Kent", age=9)
            db.session.add(clark)
            db.session.commit()

            response = app.test_client().get('/campers').json
            campers = Camper.query.all()
            assert [camper['id'] for camper in response] == [camper.id for camper in campers]
            assert [camper['name'] for camper in response] == [camper.name for camper in campers]
            assert [camper['age'] for camper in response] == [camper.age for camper in campers]


    def test_gets_camper_by_id(self):
        '''retrieves one camper using its ID with GET request to /campers/<int:id>.'''

        with app.app_context():
            bruce = Camper(name="Bruce Wayne", age=11)
            db.session.add(bruce)
            db.session.commit()

            response = app.test_client().get(f'/campers/{bruce.id}').json
            assert response['name'] == bruce.name
            assert response['age'] == bruce.age

    def test_returns_404_if_no_camper(self):
        '''returns an error message and 404 status code when a camper is searched by a non-existent ID.'''
        
        with app.app_context():
            Camper.query.delete()
            db.session.commit()

            response = app.test_client().get('/campers/1')
            assert response.json.get('error')
            assert response.status_code == 404

    def test_creates_camper(self):
        '''creates one camper using a name and age with a POST request to /campers.'''

        with app.app_context():
            Camper.query.delete()
            db.session.commit()

            response = app.test_client().post(
                'campers',
                json={
                    'name': 'Tony Stark',
                    'age': 15
                }
            ).json

            assert response['id']
            assert response['name'] == 'Tony Stark'
            assert response['age'] == 15

            tony = Camper.query.filter(Camper.name=='Tony Stark', Camper.age==15).one_or_none()
            assert tony

    def test_gets_activities(self):
        '''retrieves activities with GET request to /activities'''

        with app.app_context():
            activity = Activity(name="Swimming", difficulty="4")
            db.session.add(activity)
            db.session.commit()

            response = app.test_client().get('/activities').json
            activities = Activity.query.all()

            assert [activity['id'] for activity in response] == [activity.id for activity in activities]
            assert [activity['name'] for activity in response] == [activity.name for activity in activities]
            assert [activity['difficulty'] for activity in response] == [activity.difficulty for activity in activities]
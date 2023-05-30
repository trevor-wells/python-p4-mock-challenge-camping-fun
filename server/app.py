#!/usr/bin/env python3

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}")

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Activity, Camper, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api=Api(app)


class Index(Resource):

    def get(self):
        return "help!", 911

class Campers(Resource):

    def get(self):
        response = [{'id': camper.id, 'name': camper.name, 'age': camper.age} for camper in Camper.query.all()]
        return make_response(response, 200)

    def post(self):
        try: 
            new_camper = Camper(
                name = request.get_json()['name'],
                age = request.get_json()['age']
            )
            db.session.add(new_camper)
            db.session.commit()
            return new_camper.to_dict(), 201
        except ValueError:
            return {"error": "400: Validation error"}, 400
        
class CamperById(Resource):
    
    def get(self, id):
        camper = Camper.query.filter_by(id=id).first()
        if camper:
            return make_response(camper.to_dict(), 200)
        return make_response({"error": "404: Camper not found"}, 404)
    
class Activities(Resource):
    
    def get(self):
        activities = [{'id': activity.id, 'name': activity.name, 'difficulty': activity.difficulty} for activity in Activity.query.all()]
        return make_response(activities, 200)

class ActivityById(Resource):
    
    def get(self, id):
        activity = Activity.query.filter(Activity.id == id).first()
        if activity:
            return activity.to_dict(), 200
        return {"error": "404: FUCK OFFFFFFFFFFFFF"}, 404
    
    def delete(self, id):
        activity = Activity.query.filter_by(id=id).first()
        if activity:
            for signup in activity.signups:
                db.session.delete(signup)
            db.session.commit()
            db.session.delete(activity)
            db.session.commit()
            return {}, 204
        return {"error": "404: Activity not found"}, 404
        
class Signups(Resource):
    
    def post(self):
        
        try:
            new_signup = Signup(
                time = request.get_json()['time'],
                camper_id = request.get_json()['camper_id'],
                activity_id = request.get_json()['activity_id']
            )
            db.session.add(new_signup)
            db.session.commit()
            return new_signup.to_dict(), 201
        except ValueError:
            return {"error": "400: Validation error"}, 400
    
api.add_resource(Index, '/')
api.add_resource(Campers, '/campers')
api.add_resource(CamperById, '/campers/<int:id>')
api.add_resource(Activities, '/activities')
api.add_resource(Signups, '/signups')
api.add_resource(ActivityById, '/activities/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

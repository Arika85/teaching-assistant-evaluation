# importing the libraries
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import os

# basedir for database
basedir = os.path.abspath(os.path.dirname(__file__))

# instantiating the app
app = Flask(__name__)
# instantiating the api
api = Api(app)

# configuration
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# creating the model for database
class TaeTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    native_english_speaker = db.Column(db.Integer, nullable=False)
    course_instructor = db.Column(db.Integer, nullable=False)
    course = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    class_size = db.Column(db.Integer, nullable=False)
    
# creating database 
# with app.app_context():
#     db.create_all()


task_post_args = reqparse.RequestParser()
task_post_args.add_argument("native_english_speaker", type=int, help="This field is required", required=True)
task_post_args.add_argument("course_instructor", type=int, help="This field is required", required=True)
task_post_args.add_argument("course", type=int, help="This field is required", required=True)
task_post_args.add_argument("semester", type=int, help="This field is required", required=True)
task_post_args.add_argument("class_size", type=int, help="This field is required", required=True)

task_put_args = reqparse.RequestParser()
task_put_args.add_argument("native_english_speaker", type=int)
task_put_args.add_argument("course_instructor", type=int)
task_put_args.add_argument("course", type=int)
task_put_args.add_argument("semester", type=int)
task_put_args.add_argument("class_size", type=int)

# defining the fields
resource_fields = {
  "id": fields.Integer,
  "native_english_speaker" : fields.Integer,
  "course_instructor" : fields.Integer,
  "course" : fields.Integer,
  "semester" : fields.Integer,
  "class_size" : fields.Integer,
}

# method for listing all the data
class Tae_CRUD_List(Resource):
    def get(self):
        tasks = TaeTable.query.all()
        all_data = {}
        for task in tasks:
            all_data[task.id] = {"native_english_speaker": task.native_english_speaker, "course_instructor":task.course_instructor,
                            "course":task.course, "semester": task.semester, "class_size": task.class_size}
        return all_data

# class for CRUD method
class Tae_CRUD(Resource):
    # get method function
    @marshal_with(resource_fields)
    def get(self, id):
        task = TaeTable.query.filter_by(id=id).first()
        if not task:
            abort(404, message="Could not find data with that id")
        return task

    # post method
    @marshal_with(resource_fields)
    def post(self, id):
        args = task_post_args.parse_args()
        task = TaeTable.query.filter_by(id=id).first()
        if task:
            abort(409, message="This id is taken!")
        
        info = TaeTable(id=id, native_english_speaker=args['native_english_speaker'], course_instructor=args['course_instructor'], 
                            course=args['course'], semester=args['semester'], class_size=args['class_size'])
        db.session.add(info)
        db.session.commit()
        return info, 201

    # put method
    @marshal_with(resource_fields)
    def put(self, id):
        args = task_put_args.parse_args()
        task = TaeTable.query.filter_by(id=id).first()

        if not task:
            abort(404, message="Data doesn't exist, cannot update!")
        if args['native_english_speaker']:
            task.native_english_speaker = args['native_english_speaker']
        if args['course_instructor']:
            task.course_instructor = args['course_instructor']
        if args['course']:
            task.course = args['course']
        if args['semester']:
            task.semester = args['semester']
        if args['class_size']:
            task.class_size = args['class_size']
        db.session.commit()
        return task

    # delete method
    def delete(self, id):
        task = TaeTable.query.filter_by(id=id).first()
        db.session.delete(task)
        return 'Data Deleted', 204
           
# endpoints for api
api.add_resource(Tae_CRUD, '/crudop/<int:id>')
api.add_resource(Tae_CRUD_List, '/crudop')

if __name__ == '__main__':
    app.run(debug=False)

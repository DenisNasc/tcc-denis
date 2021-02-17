import os

from flask import Flask, g
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f'sqlite:///{os.path.join(basedir, "data.sqlite")}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app_context = app.app_context()
app_context.push()


db = SQLAlchemy(app)
api = Api(app)

g.db = db
g.api = api
migrate = Migrate(app, db)


from routes.users import Users
from routes.projects import Projects
from routes.stations import Stations

api.add_resource(Users, "/users/<id>", "/users")
api.add_resource(
    Projects, "/users/<user_id>/projects/<id>", "/users/<user_id>/projects"
)
api.add_resource(
    Stations,
    "/users/<user_id>/projects/<project_id>/stations/<id>",
    "/users/<user_id>/projects/<project_id>/stations",
)

if __name__ == "__main__":
    app.run(debug=True)

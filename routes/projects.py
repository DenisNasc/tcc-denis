from flask import g
from flask_restful import Resource, reqparse, fields, marshal_with
from models.projects import Project
from models.users import User

db = g.db

response_fields = {
    "id": fields.String,
    "user_id": fields.String,
    "name": fields.String,
    "message": fields.String,
    # "projects": {"id": fields.String},
}


def init_args(fields):
    parser = reqparse.RequestParser()

    for field in fields:
        parser.add_argument(field)

    args = parser.parse_args()
    return args


# APRENDER A RETORNAR OBJETOS EM UMA LISTA


class Projects(Resource):
    @marshal_with(response_fields)
    def get(self, user_id, id):
        # if id == "1":
        #     projects = Project.query.filter_by(user_id=user_id).all()
        #     print(projects[0])
        #     return {"projects": projects[0]}, 200, {}

        # project = Project.query.filter_by(user_id=user_id, id=id).first()
        # print(project)
        return {}, 200, {}

    @marshal_with(response_fields)
    def post(self, user_id):
        fields = ("name", "length_overall", "length_perpendiculars", "breadth", "draft")
        args = init_args(fields)

        user = User.query.filter_by(id=user_id).first()

        if not user:
            response = {"message": "Usuário não existe"}

            return response, 400, {}

        name = Project.query.filter_by(name=args.name).first()

        if name:
            response = {"message": "Ja existe um projeto com esse nome"}

            return response, 409, {}

        new_project = Project(**args, user_id=user_id)

        db.session.add(new_project)
        db.session.commit()

        return new_project, 201, {}
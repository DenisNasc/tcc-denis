from flask import g
from flask_restful import Resource, reqparse, fields, marshal_with
from models.users import User

db = g.db

response_fields = {
    "id": fields.String,
    "username": fields.String,
    "message": fields.String,
}


def init_args(fields):
    parser = reqparse.RequestParser()

    for field in fields:
        parser.add_argument(field)

    args = parser.parse_args()
    return args


class Users(Resource):
    @marshal_with(response_fields)
    def get(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            if not user:
                response = {}
                return response, 400, {}

            response = user
            return response, 200, {}
        except:
            response = {"message": "Um erro inesperado ocorreu no servidor!"}
            return response, 500, {}

    @marshal_with(response_fields)
    def post(self):

        print("args")
        fields = ("username", "email", "password")
        args = init_args(fields)

        username = User.query.filter_by(username=args.username).first()
        email = User.query.filter_by(username=args.email).first()
        if email or username:
            status_code = 409
            responde_headers = {}
            response = {"message": "Ja existe um usuário com esses dados"}

            return response, status_code, responde_headers

        new_user = User(**args)

        db.session.add(new_user)
        db.session.commit()

        response = new_user

        return response, 201, {}

    @marshal_with(response_fields)
    def put(self, id):
        try:
            fields = ("username", "email", "password")
            args = init_args(fields)

            user = User.query.filter_by(id=id).first()

            if not user:
                response = {"message": "Não existe um usuário com esses dados"}

                return response, 400, {}

            user.username = args.username
            user.email = args.email
            user.password = args.password
            db.session.commit()

            response = {}

            return response, 204, {}
        except:
            response = {"message": "Um erro inesperado ocorreu no servidor!"}
            return response, 500, {}

    @marshal_with(response_fields)
    def delete(self, id):
        try:
            user = User.query.filter_by(id=id).first()
            if not user:
                response = {"message": "Este usuário não existe"}
                return response, 400, {}
            db.session.delete(user)
            db.session.commit()
        except:
            response = {"message": "Um erro inesperado ocorreu no servidor!"}
            return response, 500, {}
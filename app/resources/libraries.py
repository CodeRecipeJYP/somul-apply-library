import json

from flask import jsonify, Blueprint
from flask_restful import Resource, reqparse, Api, fields, marshal_with

from app import db
from app.database.models import Library


library_fields = {
    '_id': fields.Integer,
    'name': fields.String,
    'location_road': fields.String,
    'location_number': fields.String,
    'location_detail': fields.String,

    'manager_name': fields.String,
    'manager_email': fields.String,
    'manager_phone': fields.String,
    'audiences': fields.String,

    'fac_beam_screen': fields.Boolean,
    'fac_sound': fields.Boolean,
    'fac_record': fields.Boolean,
    'fac_placard': fields.Boolean,
    'fac_self_promo': fields.Boolean,

    'fac_other': fields.String,
    'req_speaker': fields.String,
}


class LibraryListResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, trim=True)
        self.reqparse.add_argument('location_road', type=str, trim=True)
        self.reqparse.add_argument('location_number', type=str, trim=True)
        self.reqparse.add_argument('location_detail', type=str, trim=True)

        self.reqparse.add_argument('manager_name', type=str, trim=True)
        self.reqparse.add_argument('manager_email', type=str, trim=True)
        self.reqparse.add_argument('manager_phone', type=str, trim=True)
        self.reqparse.add_argument('audiences', type=str, trim=True)

        self.reqparse.add_argument('fac_beam_screen', type=bool)
        self.reqparse.add_argument('fac_sound', type=bool)
        self.reqparse.add_argument('fac_record', type=bool)
        self.reqparse.add_argument('fac_placard', type=bool)
        self.reqparse.add_argument('fac_self_promo', type=bool)

        self.reqparse.add_argument('fac_other', type=str, trim=True)
        self.reqparse.add_argument('req_speaker', type=str, trim=True)
        super().__init__()

    @marshal_with(library_fields)
    def get(self):
        libraries = db.query(Library).all()
        return libraries

    @marshal_with(library_fields)
    def post(self):
        args = self.reqparse.parse_args()
        library = Library(**args)
        db.add(library)
        try:
            db.commit()

            return library

        except:  # noqa: E722
            db.rollback()
            print("Unexpected DB server error")
            return json.dumps({
                "result": 1,
                "cause": "Unexpected DB server error"
            })
        # db.add_all([
        #     Library(
        #         name=args["name"],
        #         location_road=args["roadAddress"],
        #         location_number=args["numberAddress"],
        #         location_detail=args["detailAddress"],
        #         manager_name=args["managerName"],
        #         manager_email=args["managerEmail"],
        #         manager_phone=args["managerPhone"],
        #         audiences=args["capacity"],
        #         fac_beam_screen=1 if args["facilityBeamOrScreen"] else 0,
        #         fac_sound=1 if args["facilitySound"] else 0,
        #         fac_record=1 if args["facilityRecord"] else 0,
        #         fac_placard=1 if args["facilityPlacard"] else 0,
        #         fac_self_promo=1 if args["facilitySelfPromo"] else 0,
        #         fac_other=args["facilityOther"],
        #         req_speaker=args["requirements"]
        #     )
        # ])
        #
        # try:
        #     db.commit()
        #
        #     return json.dumps({
        #         "result": 0
        #     })
        # except:  # noqa: E722
        #     db.rollback()
        #     print("Unexpected DB server error")
        #     return json.dumps({
        #         "result": 1,
        #         "cause": "Unexpected DB server error"
        #     })


class LibraryResource(Resource):
    def get(self, id):
        return jsonify({'library': 1})

    def put(self, id):
        return jsonify({'library': 1})

    def delete(self, id):
        return jsonify({'library': 1})


libraries_api = Blueprint('resources.libraries', __name__)
api = Api(libraries_api)
api.add_resource(
    LibraryListResource,
    '/library',
    endpoint='libraries'
)

api.add_resource(
    LibraryResource,
    '/library/<int:id>',
    endpoint='library'
)

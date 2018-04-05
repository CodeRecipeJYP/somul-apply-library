import json
import traceback

from flask import jsonify, Blueprint
from flask_restful import Resource, reqparse, Api

from app import db
from app.database import models


class LibraryList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    def get(self):
        libraries = models.Library.query.all()
        return jsonify(libraries)

    def post(self):
        args = self.reqparse.parse_args()

        db.add_all([
            Library(
                name=args["name"],
                location_road=args["roadAddress"],
                location_number=args["numberAddress"],
                location_detail=args["detailAddress"],
                manager_name=args["managerName"],
                manager_email=args["managerEmail"],
                manager_phone=args["managerPhone"],
                audiences=args["capacity"],
                fac_beam_screen=1 if args["facilityBeamOrScreen"] else 0,
                fac_sound=1 if args["facilitySound"] else 0,
                fac_record=1 if args["facilityRecord"] else 0,
                fac_placard=1 if args["facilityPlacard"] else 0,
                fac_self_promo=1 if args["facilitySelfPromo"] else 0,
                fac_other=args["facilityOther"],
                req_speaker=args["requirements"]
            )
        ])

        try:
            db.commit()

            return json.dumps({
                "result": 0
            })
        except:  # noqa: E722
            db.rollback()
            print("Unexpected DB server error")
            return json.dumps({
                "result": 1,
                "cause": "Unexpected DB server error"
            })


class Library(Resource):
    def get(self, id):
        return jsonify({'library': 1})

    def put(self, id):
        return jsonify({'library': 1})

    def delete(self, id):
        return jsonify({'library': 1})


libraries_api = Blueprint('resources.libraries', __name__)
api = Api(libraries_api)
api.add_resource(
    LibraryList,
    '/library',
    endpoint='libraries'
)

api.add_resource(
    Library,
    '/library/<int:id>',
    endpoint='library'
)

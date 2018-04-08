from flask import Blueprint
from flask_restful import Resource, reqparse, fields, marshal_with, Api
from sqlalchemy.exc import IntegrityError

from app import db
from app.database.models import Library
from app.resources.errors import DuplicatedDataError, DataNotFoundError

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


libraryReqparse = reqparse.RequestParser()
libraryReqparse.add_argument('name', type=str,
                             location=['form', 'json'],
                             required=True,
                             nullable=False,
                             help='No library name provided')
libraryReqparse.add_argument('location_road', type=str, trim=True)
libraryReqparse.add_argument('location_number', type=str, trim=True)
libraryReqparse.add_argument('location_detail', type=str, trim=True)

libraryReqparse.add_argument('manager_name', type=str, trim=True)
libraryReqparse.add_argument('manager_email', type=str, trim=True)
libraryReqparse.add_argument('manager_phone', type=str, trim=True)
libraryReqparse.add_argument('audiences', type=str, trim=True)

libraryReqparse.add_argument('fac_beam_screen', type=bool)
libraryReqparse.add_argument('fac_sound', type=bool)
libraryReqparse.add_argument('fac_record', type=bool)
libraryReqparse.add_argument('fac_placard', type=bool)
libraryReqparse.add_argument('fac_self_promo', type=bool)

libraryReqparse.add_argument('fac_other', type=str, trim=True)
libraryReqparse.add_argument('req_speaker', type=str, trim=True)


def get_or_404(clazz, pk):
    instance = db.query(clazz).filter_by(_id=pk).first()
    if instance is None:
        raise DataNotFoundError("Library {} Not found".format(pk))

    return instance


class LibraryListResource(Resource):
    def __init__(self):
        super().__init__()

    @marshal_with(library_fields)
    def get(self):
        libraries = db.query(Library).all()
        return libraries

    @marshal_with(library_fields)
    def post(self):
        args = libraryReqparse.parse_args()

        library = Library(**args)

        try:
            db.add(library)
            db.commit()
        except IntegrityError as e:
            print(str(e))
            db.rollback()
            raise DuplicatedDataError(str(e.orig))
        except Exception as e:
            print(str(e))
            db.rollback()
            raise e

        return library


class LibraryResource(Resource):
    @marshal_with(library_fields)
    def get(self, pk):
        library = get_or_404(Library, pk)
        return library

    @marshal_with(library_fields)
    def put(self, pk):
        args = libraryReqparse.parse_args()
        library = get_or_404(Library, pk)

        for key, value in args.items():
            if value is None:
                continue

            setattr(library, key, value)

        try:
            db.merge(library)
            db.commit()
        except IntegrityError as e:
            print(str(e))
            db.rollback()
            raise DuplicatedDataError(str(e.orig))
        except Exception as e:
            print(str(e))
            db.rollback()
            raise e

        return library

    def delete(self, pk):
        library = get_or_404(Library, pk)

        try:
            db.delete(library)
            db.commit()
        except Exception as e:
            print(str(e))
            db.rollback()
            raise e

        return '', 204


libraries_api = Blueprint('resources.libraries', __name__)
api = Api(libraries_api)
api.add_resource(
    LibraryListResource,
    '/library',
    endpoint='libraries'
)

api.add_resource(
    LibraryResource,
    '/library/<int:pk>',
    endpoint='library'
)

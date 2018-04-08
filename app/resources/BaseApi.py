from flask_restful import Api, abort
from werkzeug.exceptions import HTTPException


class InvalidArgumentError(HTTPException):
    code = 400
    pass


# custom_errors = {
#     'InvalidArgumentError': {
#         'message': "InvalidArgumentError",
#         'status': 400,
#     }
# }


class BaseApi(Api):
    # def __init__(self, app=None, prefix='', default_mediatype='application/json', decorators=None, catch_all_404s=False,
    #              serve_challenge_on_401=False, url_part_order='bae', errors=custom_errors):
    #     super().__init__(app, prefix, default_mediatype, decorators, catch_all_404s, serve_challenge_on_401,
    #                      url_part_order, errors)

    def error_router(self, original_handler, e):
        # if type(e) is InvalidArgumentError:
        #     abort(400, message="Invalid Arguments")

        return original_handler(e)

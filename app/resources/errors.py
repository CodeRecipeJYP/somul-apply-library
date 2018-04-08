from werkzeug.exceptions import HTTPException


class InvalidArgumentError(HTTPException):
    code = 400


class DuplicatedDataError(HTTPException):
    code = 400


class DataNotFoundError(HTTPException):
    code = 404

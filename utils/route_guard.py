import functools

from fastapi.responses import JSONResponse

from utils.helpers import hash_password


def check_user_credentials(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        from server import database
        from routes.profile.router import ResponseBody

        request = kwargs['body']
        stored_user = database.get_user(request.email)
        if not stored_user:
            return JSONResponse(status_code=404, content=ResponseBody(success=False, message='user not found').dict())
        if stored_user.password != hash_password(request.password):
            return JSONResponse(status_code=401, content=ResponseBody(success=False, message='wrong password').dict())
        return fn(*args, **kwargs)
    return wrapper


def check_user_logged_in(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        from server import database
        from routes.profile.router import ResponseBody

        request = kwargs['body']
        stored_user = database.get_user(request.email)
        if stored_user.session_id:
            return fn(*args, **kwargs)
        return JSONResponse(status_code=401, content=ResponseBody(success=False, message='not logged in').dict())
    return wrapper


# def check_session_id(fn):
#     @functools.wraps(fn)
#     def wrapper(*args, **kwargs):
#         from server import database

#         request = kwargs['request']
#         request.cookies.get('session_id')


from fastapi import Request
from functools import wraps
from .exceptions import LoginRequiredException


def login_required(func):
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        # session_token = request.cookies.get('session_id')
        # user_session = verify_user_id(session_token)
        if not request.user.is_authenticated:
            raise LoginRequiredException(status_code=401)
        return func(request, *args, **kwargs)
    return wrapper
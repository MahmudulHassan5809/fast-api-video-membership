from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.middleware.authentication import AuthenticationMiddleware

from cassandra.cqlengine.management import sync_table

from app.users.backens import JWTCookieBackend

from . import db
from .users.models import User
from .videos.models import Video
from .users.views import router as user_router





app = FastAPI()

app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend)

from .handlers import * # noqa

DB_SESSION = None

@app.on_event("startup")
def on_startup():
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)
    sync_table(Video)




app.include_router(user_router)
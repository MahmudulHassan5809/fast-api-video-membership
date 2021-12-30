from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from cassandra.cqlengine.management import sync_table

from . import db
from .users.models import User
from .users.views import router as user_router




app = FastAPI()

DB_SESSION = None

@app.on_event("startup")
def on_startup():
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)




app.include_router(user_router)
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.middleware.authentication import AuthenticationMiddleware

from cassandra.cqlengine.management import sync_table

from app.users.backens import JWTCookieBackend

from . import db
from .users.models import User
from .videos.models import Video
from .watch_events.models import WatchEvent
from .playlists.models import Playlist
from .users.views import router as user_router
from .videos.views import router as video_router
from .watch_events.views import router as event_router
from .playlists.views import router as platlist_router
from .indexing.client import (
    update_index,
    search_index
)


app = FastAPI()

app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())

from .handlers import *  # noqa

DB_SESSION = None


@app.on_event("startup")
def on_startup():
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)
    sync_table(Video)
    sync_table(WatchEvent)
    sync_table(Playlist)


app.include_router(user_router)
app.include_router(video_router)
app.include_router(event_router)
app.include_router(platlist_router)


@app.post('/update-index', response_class=HTMLResponse)
def htmx_update_index_view(request: Request):
    count = update_index()
    return HTMLResponse(f"({count}) Refreshed")


@app.get("/search", response_class=HTMLResponse)
def search_detail_view(request: Request, q: Optional[str] = None):
    query = None
    context = {}
    if q is not None:
        query = q
        results = search_index(query)
        hits = results.get('hits') or []
        num_hits = results.get('nbHits')
        context = {
            "query": query,
            "hits": hits,
            "num_hits": num_hits
        }
    return render(request, "search/detail.html", context)

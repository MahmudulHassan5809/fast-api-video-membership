from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from app.videos.models import Video

from app.videos.schemas import VideoCreateSchema
from app.users.decorators import login_required
from app.shortcuts import redirect, render
from app import utils

router = APIRouter(
    prefix="/videos",
    tags=['Videos']
)


@router.get("/create", response_class=HTMLResponse)
@login_required
def video_create_view(request: Request):
    return render(request, "videos/create.html", {})


@router.post("/create", response_class=HTMLResponse)
@login_required
def video_create_post_view(request: Request, title: str = Form(...), url: str = Form(...)):
    raw_data = {
        "title": title,
        "url": url,
        "user_id": request.user.username
    }
    data, errors = utils.valid_schema_data_or_error(
        raw_data, VideoCreateSchema)

    context = {
        "data": data,
        "errors": errors,
        "title": title,
        "url": url,
    }
    if len(errors) > 0:
        return render(request, "videos/create.html", context, status_code=400)

    redirect_path = data.get('path') or "/videos/create"
    return redirect(redirect_path)


@router.get("/list", response_class=HTMLResponse)
def video_list_view(request: Request):
    q = Video.objects.all().limit(100)
    context = {
        "object_list": q
    }
    return render(request, "videos/list.html", context)


@router.get("/")
def video_detail_view(request: Request, response_class=HTMLResponse):
    return render(request, "videos/detail.html", {})

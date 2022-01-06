from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.shortcuts import  render


router = APIRouter(
    prefix="/videos",
    tags=['Videos']
)

@router.get("/")
def video_list_view(request: Request, response_class=HTMLResponse):
    return render(request, "videos/list.html", {})



@router.get("/")
def video_detail_view(request: Request, response_class=HTMLResponse):
    return render(request, "videos/detail.html", {})

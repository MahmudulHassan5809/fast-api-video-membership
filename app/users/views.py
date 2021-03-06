from fastapi import APIRouter
from fastapi.params import Depends, Form
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from .models import User
from .decorators import login_required
from .scheams import UserLoginSchema, UserResponse, UserSignupSchema
from typing import List, Optional
from .. import utils
from ..shortcuts import redirect, render


router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get('/list/', response_model=List[UserResponse])
def get_user_list():
    qs = User.objects.all()
    return list(qs)


@router.get('/login/', response_class=HTMLResponse)
def login(request: Request, ):
    context = {
        "request": request,
        "title": 'Login'
    }
    return render(request, "auth/login.html", context, status_code=200)


@router.post('/login/', response_class=HTMLResponse)
def login(request: Request,
          email: str = Form(...),
          password: str = Form(...),
          next: Optional[str] = "/"):

    raw_data = {
        "email": email,
        "password": password
    }

    data, errors = utils.valid_schema_data_or_error(raw_data, UserLoginSchema)

    context = {
        "data": data,
        "errors": errors,
        "title": 'Login'
    }

    print(errors, '------------')
    if len(errors) > 0:
        return render(request, "auth/login.html", context, status_code=400)
    if "http://127.0.0.1" not in next:
        next = '/users/profile/'
    print(next)
    return redirect(next, cookies=data)


@router.get('/register/', response_class=HTMLResponse)
def register(request: Request, ):
    context = {
        "request": request,
        "title": 'Register'
    }
    return render(request, "auth/register.html", context, status_code=200)


@router.post('/register/', response_class=HTMLResponse)
def register(request: Request,
             email: str = Form(...),
             password: str = Form(...),
             password_confirm: str = Form(...),
             next: Optional[str] = "/"):

    raw_data = {
        "email": email,
        "password": password,
        "password_confirm": password_confirm
    }

    data, errors = utils.valid_schema_data_or_error(raw_data, UserSignupSchema)
    context = {
        "data": data,
        "errors": errors,
    }
    if len(errors) > 0:
        return render(request, "auth/register.html", context, status_code=400)

    User.create_user(email=data['email'], password=password)
    return redirect("/users/login")


@router.get('/profile/', response_class=HTMLResponse)
@login_required
def profile(request: Request):
    context = {
        "title": 'Profile'
    }
    return render(request, "account/profile.html", context, status_code=200)


@router.get("/logout", response_class=HTMLResponse)
def logout_get_view(request: Request):
    if not request.user.is_authenticated:
        return redirect('/users/login')
    return render(request, "auth/logout.html", {})


@router.post("/logout", response_class=HTMLResponse)
def logout_post_view(request: Request):
    return redirect("/users/login", remove_session=True)

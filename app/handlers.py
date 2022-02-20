from starlette.exceptions import HTTPException as StartletteHTTPException


from app.main import app
from app.shortcuts import redirect, render, is_htmx
from app.users.exceptions import LoginRequiredException


@app.exception_handler(StartletteHTTPException)
async def http_exception_handler(request, exc):
    status_code = exc.status_code

    if status_code == 404:
        template_name = 'errors/404.html'

    template_name = 'errors/main.html'
    context = {"status_code": status_code}
    return render(request, template_name, context, status_code=status_code)


@app.exception_handler(LoginRequiredException)
async def login_required_exception_handler(request, exc):
    response = redirect(
        f'/users/login/?next={request.url}', remove_session=True)
    if is_htmx(request):
        response.status_code = 200
        response.headers['HX-Redirect'] = '/users/login'
    return response

import pathlib
from fastapi.templating import Jinja2Templates

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

def get_templates():
    return templates
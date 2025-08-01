from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.api_route("/", methods=["GET", "POST"], response_class=HTMLResponse)
def index(request: Request, input: str = Form(None), cap_string: str = Form(None)):
    """
    Load index.html. If a post request was sent and data has been returned, include the data in the response context.
    """
    if request.method == "GET":
        return templates.TemplateResponse(request, "index.html")
    else:
        return templates.TemplateResponse(request, "index.html", {"input": input, "cap_string": cap_string})

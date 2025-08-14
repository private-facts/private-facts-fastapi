import urllib3

from decouple import config
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .tahoe import TahoeClient

BASE_URL = config('BASE_URL')
LOCAL_BASE_URL = config('LOCAL_BASE_URL')
HTTP = urllib3.PoolManager()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

def get_tahoe_client():
    return TahoeClient(base_url=LOCAL_BASE_URL, http=HTTP)


@app.api_route("/", methods=["GET", "POST"], response_class=HTMLResponse)
def index(request: Request,
          data: str = Form(None),
          cap_string: str = Form(None),
          tahoe_client = Depends(get_tahoe_client)):
    """
    Load index.html. If a post request was sent and data has been returned, include the data in the response context.
    """
    if request.method == "GET":
        
        return templates.TemplateResponse(request, "index.html")
    
    elif data:
        try:
            cap_string = tahoe_client.post_data(data)

            return templates.TemplateResponse(request, "index.html", {"cap_string": cap_string})
        
        except Exception as e:
            print(f"An error occurred: {e}")
            error_context = {
                "type": type(e).__name__,
                "message": str(e)
            }

            return templates.TemplateResponse(request, "error.html", {"exception": error_context})

    elif cap_string:
        try:
            response = tahoe_client.get_data(cap_string)
            data = response[0]
            return templates.TemplateResponse(request, "index.html", {"data": data})
        
        except Exception as e:
            print(f"An error occurred: {e}")
            error_context = {
                "type": type(e).__name__,
                "message": str(e)
            }
            return templates.TemplateResponse(request, "error.html", {"exception": error_context})

    return templates.TemplateResponse(request, "index.html")

from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
import uvicorn
import json
from ipc import client_program
from translate import translatedWords

trans = translatedWords('fr')

templates = Jinja2Templates(directory='templates')


async def homepage(request):
    template = "index.html"
    context = {"request": request}
    context['trans'] = trans
    return templates.TemplateResponse(template, context)


async def messages(request):
    template = "messages.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)


async def envSelected(request):
    global trans
    """Handles request to spin up a new ENV

        :param dic request: the request sent by GET

        :returns: new HTML

        :rtype: HTML
    """
    template = "envSelected.html"
    context = {"request": request}
    requestDic = vars(request)
    context["query_string"] = str(requestDic["scope"]["query_string"], 'UTF-8')[-1]
    launcherMsg = client_program('up', 'user1', 'ENV1')
    context['launcherMsg'] = launcherMsg
    context['trans'] = trans
    return templates.TemplateResponse(template, context)


async def stopEnv(request):
    template = "stopEnv.html"
    context = {"request": request}
    launcherMsg = client_program('down', 'user1', 'ENV1')
    context['launcherMsg'] = launcherMsg
    return templates.TemplateResponse(template, context)


async def error(request):
    """
    An example error. Switch the `debug` setting to see either tracebacks or 500 pages.
    """
    raise RuntimeError("Oh no")


async def not_found(request: Request, exc: HTTPException):
    """
    Return an HTTP 404 page.
    """
    template = "404.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=404)


async def server_error(request: Request, exc: HTTPException):
    """
    Return an HTTP 500 page.
    """
    template = "500.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context, status_code=500)


routes = [
    Route('/', homepage),
    Route('/messages', messages),
    Route('/envSelected', envSelected),
    Route('/stopEnv', stopEnv),
    Route('/error', error),
    Mount('/static', app=StaticFiles(directory='static'), name="static")
]

exception_handlers = {
    404: not_found,
    500: server_error
}

app = Starlette(debug=True, routes=routes, exception_handlers=exception_handlers)


# Not currently used as cannot do reload with below method, only from command line
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=80)


def testThing():
    """ Test

        :returns: 2

        :rtype: int
    """
    print("test")
    return 2
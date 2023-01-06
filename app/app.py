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
import signal
from starlette.responses import PlainTextResponse, RedirectResponse

language: str = 'en'
trans = translatedWords(language)

templates = Jinja2Templates(directory='templates')


networks = {
    'hospitals': {
        1 : {
            'name': 'Meadow Brook Hospital', 'epr':'Nexus', 'pas': 'Wards', 'pacs':'Spark', 'tie':'Echo', 'profilePic':'MeadowBrookHospital.jpg'
        },
        2 : {
             'name':'Sutton Bridge Hospital', 'epr':'Nexus', 'pas': 'Cygnus', 'pacs':'Quantum', 'tie':'Flux', 'profilePic':'SuttonBridgeHospital.jpg'
        },
        3 : {
            'name':'Rose Hill Hospital', 'epr':'AHHI', 'pas': 'Cygnus', 'pacs':'Spark', 'tie':'Velocity', 'profilePic':'RoseHillHospital.jpg'
        },
        4 : {
            'name': 'Millfield Hospital', 'epr':'Nexus', 'pas': 'Wards', 'pacs':'Quantum', 'tie':'Echo', 'profilePic':'MillfieldHospital.jpg'
        }
    },
    'gps': {
        'Farm View Surgery' : {
            'epr':'YRHealth'
        },
        'Hill Springs Surgery' : {
            'epr':'ESSE'
        },
        'Cats Eye Surgery' : {
            'epr':'Atom'
        },
        'Jump Gate Surgery' : {
            'epr':'Atom'
        }
    },
    'socialCare': {
        'Ashtonshire Care' : {
            'hub': 'County Connex'
        },
        'Westbridgeshire Area' : {
            'hub': 'County Connex'
        },
        'Briarwoodshire Together' : {
            'hub': 'JUTS'
        },
        'Mapleshire Towns' : {
            'hub': 'JUTS'
        }
    },
    'industry': {
        'Eclipse Enterprises' : {
            'products': 'EPR, PACS, PAS'
        },
        'Skyline Solutions' : {
            'products': 'PAS'
        },
        'Summit Technologies' : {
            'products': 'Personal health apps'
        },
        'Horizon Holdings' : {
            'products': 'TIE'
        }
    }
}


#print(networks)

def handler_stop_signals(signum, frame):
    """MKDOCS STD: Catch SIGTERM from 'docker-compose down', to gracefully close down all containers started by launcher
        
        Args:
            signum: something to do with signum
            frame: something to do with frame
        Returns:
            nothing -> system exits
    """

    global runningENVs, exitFlag
    logMsg("Closing down App")
    sys.exit(0)


signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)



async def homepage(request):
    """Home page

        Args:
            request: request results from client
        Returns:
            Home page
    """

    template = "index.html"
    context = {"request": request}
    context['trans'] = trans
    return templates.TemplateResponse(template, context)


async def messages(request):
    """messages test

        Args:
            request: request results from client
        Returns:
            test message
    """
    template = "messages.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)


async def envSelected(request):
    """ENV selected function. Sends message to launcher container to start a ENV

        Args:
            request: request results from client
        Returns:
            message from launcher
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
    """Spin down ENV

        Args:
            request: request results from client
        Returns:
            return message from launcher container
    """

    template = "stopEnv.html"
    context = {"request": request}
    launcherMsg = client_program('down', 'user1', 'ENV1')
    context['launcherMsg'] = launcherMsg
    return templates.TemplateResponse(template, context)


async def settings(request):
    """Loads settings html into main body of page

        Args:
            request: request results from client
        Returns:
            settings main body
    """

    template = "settings.html"
    context = {"request": request}
    context['trans'] = trans
    selectedLang = {'en': '', 'fi' : '', 'fr' : '', 'it' : '', 'sv' : ''}
    selectedLang[language] = 'selected'
    context['selected'] = selectedLang
    return templates.TemplateResponse(template, context)


async def changeLanguage(request):
    """Changes the language and reloads the page in the new language

        Args:
            request: request results from client
        Returns:
            Home page in new language
    """

    global translatedWords, language, trans

    template = "reload.html"
    context = {"request": request}

    selectedLang = {'en': '', 'fi' : '', 'fr' : '', 'it' : '', 'sv' : ''}
    selectedLang[language] = 'selected'
    context['selected'] = selectedLang

    try:
        language = request.query_params['select-2']
        trans = translatedWords(language)
    except:
        print('Error with language selected!')

    #context['trans'] = trans
    return templates.TemplateResponse(template, context)


async def network(request):
    """Network page (just started on this work)

        Args:
            request: request results from client
        Returns:
            Home page
    """

    template = "network.html"
    context = {"request": request}
    context['trans'] = trans
    context['entity'] = networks['hospitals']
    return templates.TemplateResponse (template, context)


async def commandLine(request):
    """Test page for the command line link

        Args:
            request: request results from client
        Returns:
            Command line HTMX result
    """

    template = "commandLine.html"
    context = {"request": request}
    context['trans'] = trans
    return templates.TemplateResponse (template, context)

async def error(request):
    """An example error. Switch the `debug` setting to see either tracebacks or 500 pages.

        Args:
            request: request results from client
        Returns:
            raises an error

    """

    raise RuntimeError("Oh no")


async def not_found(request: Request, exc: HTTPException):
    """404 page

        Args:
            request: request results from client
        Returns:
            Home page
    """

    template = "404.html"
    context = {"request": request}
    context['trans'] = trans
    return templates.TemplateResponse(template, context, status_code=404)


async def server_error(request: Request, exc: HTTPException):
    """Server error page

        Args:
            request: request results from client
        Returns:
            Home page
    """

    template = "500.html"
    context = {"request": request}
    context['trans'] = trans
    return templates.TemplateResponse(template, context, status_code=500)



routes = [
    Route('/', homepage),
    Route('/messages', messages),
    Route('/envSelected', envSelected),
    Route('/stopEnv', stopEnv),
    Route('/settings', settings),
    Route('/changeLanguage', changeLanguage),
    Route('/network', network),
    Route('/commandLine', commandLine),


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

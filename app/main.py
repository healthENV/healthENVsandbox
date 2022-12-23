from starlette.applications import Starlette
from starlette.responses import JSONResponse

app = Starlette()

@app.route("/{name}", methods=['GET'])
async def say_hello(request):
    name = request.path_params['name']
    return JSONResponse({'message': 'Hello,' + name})
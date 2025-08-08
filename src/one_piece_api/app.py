from http import HTTPStatus

from fastapi import FastAPI

app = FastAPI(version='v0.1.0')


@app.get('/', status_code=HTTPStatus.OK)
def API_version():
    return {'version': app.version}

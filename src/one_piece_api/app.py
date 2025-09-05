from fastapi import FastAPI

from one_piece_api.routers import auth, users
from one_piece_api.schemas.API_version_schema import Version

app = FastAPI(version='v0.0.3', title='One Piece API')
app.include_router(auth.router)
app.include_router(users.router)


@app.get('/version', status_code=200, response_model=Version, tags=['Version'])
def API_version():
    return {'version': app.version}

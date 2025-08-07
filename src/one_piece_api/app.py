from fastapi import FastAPI

app = FastAPI(version='v0.1.0')


@app.get('/')
def version_API():
    return {'version': 'v0.1.0'}

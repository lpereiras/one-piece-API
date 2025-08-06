from fastapi import FastAPI 

app = FastAPI(version = "v0.1.0")

@app.get('/')
async def testing_API():
  return {'version:', app.version}
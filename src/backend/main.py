from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
import uvicorn
from starlette import status
from starlette.responses import JSONResponse

app = FastAPI(title="LibraryAPI", description="API for Library", version="1.0.0")

# Router aus den Modulen einbinden
# app.include_router(name.router)

@app.get("/")
def root():
    return {"message": "Besuche /docs für die Swagger-UI"}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.10", port=8000)
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routers import asianews_router
from routers import guardian_router
import logging


app = FastAPI(debug=True)
app.include_router(asianews_router.router)
app.include_router(guardian_router.router)

@app.get("/")
def redirect_docs():
    return RedirectResponse(url="/docs")

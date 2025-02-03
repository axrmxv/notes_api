from fastapi import FastAPI
from app.api.v1.endpoints import users, notes, auth
from app.middleware.log_middleware import LoggingMiddleware


app = FastAPI(title="Notes API")
app.add_middleware(LoggingMiddleware)


app.include_router(users.router, prefix="/admin", tags=["Admin"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["Note"])
app.include_router(auth.router, tags=["Auth"])


@app.get("/")
async def main():
    return {"msg": "Welcome to Notes API"}

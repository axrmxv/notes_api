from fastapi import FastAPI
from app.api.v1.endpoints import users, notes, auth
from app.middleware.log_middleware import LoggingMiddleware
from app.db.session import init_db, engine

from contextlib import asynccontextmanager


# Контекстный менеджер для управления жизненным циклом приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()


app = FastAPI(title="Notes API", lifespan=lifespan)

app.add_middleware(LoggingMiddleware)


app.include_router(users.router, prefix="/admin", tags=["Admin"])
app.include_router(notes.router, prefix="/api/v1", tags=["Note"])
app.include_router(auth.router, tags=["Auth"])


@app.get("/")
async def main():
    return {"msg": "Welcome to Notes API"}

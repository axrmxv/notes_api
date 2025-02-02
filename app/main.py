from fastapi import FastAPI, Depends
from app.api.v1.endpoints import users, notes, auth
from fastapi.security import OAuth2PasswordBearer


app = FastAPI(title="Notes API")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(users.router, prefix="/api/v1/users")
app.include_router(notes.router, prefix="/api/v1/notes")
app.include_router(auth.router, prefix="/api/v1/auth")


@app.get("/")
async def main():
    return {"msg": "Welcome to Notes API"}


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}

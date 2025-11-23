from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Header
from pydantic import BaseModel
from database import init_db, close_db
from models import Profile

class RouteHeaders(BaseModel):
    Authorization : str

class ProfileBase(BaseModel):
    user_id : int
    name : str
    age : int
    gender : str
    sexuality : str


# this just defines the lifespan on the app, like an event, so this runs on startup, then yeilds to shutdown.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(lifespan=lifespan)

# this is just an example, may not be offical
@app.post('/profile/create')
async def profile_create(headers:Annotated[RouteHeaders, Header()], profile:ProfileBase):
    # we would call tortoise orm to create a profile if one does not exists already

    # would need to verify headers
    existing = await Profile.get_or_none(user_id=profile.user_id)
    if existing:
        return {"success": False, "message": "profile already exists", "profile": existing}
    
    new_profile = await Profile.create(
        user_id = profile.user_id,
        name = profile.name,
        age = profile.age,
        gender = profile.gender,
        sexuality = profile.sexuality
    )

    print(new_profile.id)

    return {"success": True, "profile": profile}
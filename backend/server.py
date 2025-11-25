from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import init_db, close_db
from models import Profile, Auth
import jwt
import secrets
import random

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all origins
    allow_credentials=True,
    allow_methods=["*"],        # allow all HTTP methods
    allow_headers=["*"],        # allow all headers
)

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

@app.get('/authorize')
async def authorize(code):
    if code == "fake":
        # simulate auth
        profile = {
            'user_id': random.randint   (111111111111,999999999999),
            'avatar': None
        }
        access_data = {
            'access_token': "faifhaifhashf"
        }
        web_token = secrets.token_urlsafe(32)
        # would check if one already exists and update it 
        obj = await Auth.update_or_create(
            user_id=profile['user_id'],
            access_token = access_data['access_token'],
            web_token=web_token,
            token_type='fake'
            )
        print(obj)
        
        return {'success': True, 'profile':profile, 'web_token':web_token}
    return {'code': code}

    
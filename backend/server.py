from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from tortoise.exceptions import DoesNotExist
from pydantic import BaseModel
from database import init_db, close_db
from models import Profile, Auth
import httpx
import secrets
import random
import os

CLIENT_TOKEN = os.environ.get('CLIENT_TOKEN')
CLIENT_ID = 1442284848109846598
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

class RouteHeaders(BaseModel):
    Authorization : str

class ProfileBase(BaseModel):
    user_id : int
    name : str
    age : int
    gender : str
    sexuality : str

class DiscordExchange(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str

    model_config = {
        "populate_by_name": True
    }

class DiscordProfile(BaseModel):
    id: str
    username: str
    global_name: str
    avatar: str
    email: str


# this just defines the lifespan on the app, like an event, so this runs on startup, then yeilds to shutdown.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()

async def exchange_code(code):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:3000/authorize'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    async with httpx.AsyncClient() as client:
        response = await client.post('https://discord.com/api/v10/oauth2/token', data=data, headers=headers)
        data:dict = response.json()
        if not data.get('access_token'):
            return data
        print(data)
        return DiscordExchange(**data)
    
async def get_discord_profile(access_token) -> DiscordProfile:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {access_token}'
    }
    async with httpx.AsyncClient() as client:
        response = await client.get('https://discord.com/api/v10/users/@me', headers=headers)
        data:dict = response.json()
        profile = DiscordProfile(**data)
        return profile






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
    exchange_data:DiscordExchange|dict = await exchange_code(code)
    if type(exchange_data) != DiscordExchange:
        return {'success':False, 'message':f'exchange failed! dump: {exchange_data}'}
    # use the data to get a user profile
    profile = await get_discord_profile(exchange_data.access_token)
    web_token = secrets.token_urlsafe(32)
    await Auth.update_or_create(
        user_id=profile.id,
        access_token=exchange_data.access_token,
        web_token=web_token,
        token_type=exchange_data.token_type
    )
    return {'success':True, 'profile':profile.model_dump(), 'web_token':web_token}


@app.get('/authorization')
async def check_authorization(token):
    try:
        auth = await Auth.get(web_token= token)
    except DoesNotExist as error:
        return {'success': False}
    profile = await get_discord_profile(auth.access_token)
    return {'success':True, 'profile':profile.model_dump()}

    
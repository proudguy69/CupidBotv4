from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class RouteHeaders(BaseModel):
    Authorization : str

class ProfileBase(BaseModel):
    user_id : int
    name : str
    age : int
    gender : str
    sexuality : str


# this is just an example, may not be offical
@app.post('/profile/create')
async def profile_create(headers:Annotated[RouteHeaders, Header()], profile:ProfileBase):
    # we would call tortoise orm to create a profile if one does not exists already
    print(headers.Authorization)
    return {"profile": profile}
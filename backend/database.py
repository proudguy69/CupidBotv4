# unknown if the name will stay the same

from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url="postgres://postgres:cupiddev@localhost:5432/postgres",
        modules={"models": ["models"]},
    )
    await Tortoise.generate_schemas()



async def close_db():
    await Tortoise.close_connections()
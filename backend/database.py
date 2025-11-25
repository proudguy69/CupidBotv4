# unknown if the name will stay the same

from tortoise import Tortoise, connections

async def init_db():
    await Tortoise.init(
        db_url="postgres://postgres:cupiddev@localhost:5432/postgres",
        modules={"models": ["models"]},
    )

    # clean out db for testing
    conn = connections.get('default')
    await conn.execute_query('DROP SCHEMA public CASCADE;')
    await conn.execute_query("CREATE SCHEMA public;")
    
    await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()
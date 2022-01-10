import asyncio
import os
import psutil
import asyncpg
import json


async def main():
    connection = await asyncpg.connect('postgresql://postgres:some_secret@postgresql:5432/postgres')
    await prepare_data(connection)

    print_memory_usage_in_mb()
    await read(connection)
    print_memory_usage_in_mb()

    await connection.set_type_codec("jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog")

    await read(connection)
    print_memory_usage_in_mb()

    await connection.close()


async def prepare_data(connection):
    await connection.execute("DROP TABLE IF EXISTS some_table")
    await connection.execute("""
        CREATE TABLE some_table(
            id serial PRIMARY KEY,
            data jsonb
        )
    """)
    for i in range(1000):
        await connection.execute("INSERT INTO some_table(data) VALUES($1)", '{"key":"value"}')


async def read(connection):
    for i in range(2000):
        result = await connection.fetch("SELECT data FROM some_table")
        assert len(result) > 0


def print_memory_usage_in_mb():
    process = psutil.Process(os.getpid())
    print(round(process.memory_info().rss / 1000000))


asyncio.run(main())

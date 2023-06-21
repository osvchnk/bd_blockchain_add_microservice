from fastapi import FastAPI
import asyncio

from app.rabbit.pika_consumer import PikaConsumer


app = FastAPI()

consumer = PikaConsumer()


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(consumer.consume(loop))
    await task

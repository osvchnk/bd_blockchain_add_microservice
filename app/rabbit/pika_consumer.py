import json

import aio_pika

from app.config import RABBIT_EXCHANGE, RABBIT_QUEUE, RABBIT_ROUTING_KEY
from app.services.block import BlockService


class PikaConsumer:
    def __init__(self,
                 exchange_name: str = RABBIT_EXCHANGE,
                 queue_name: str = RABBIT_QUEUE,
                 routing_key: str = RABBIT_ROUTING_KEY
                 ):
        self.connection = None
        self.channel = None
        self.exchange_name = exchange_name
        self.queue_name = queue_name
        self.routing_key = routing_key
        self.transaction_list = []
        self.service: BlockService = BlockService()

    async def process_message(self,
                              message: aio_pika.abc.AbstractIncomingMessage,
                              ) -> None:
        async with message.process():
            print("NEW MESSAGE")
            message_json = json.loads(message.body.decode())
            print(message_json['tr_hash'])
            self.transaction_list.append(message_json['tr_hash'])
            if len(self.transaction_list) >= 5:
                await self.service.create_block(self.transaction_list)
                self.transaction_list.clear()

    async def consume(self, loop):
        self.connection = await aio_pika.connect_robust(host='localhost', port=5672, loop=loop)
        self.channel = await self.connection.channel()

        exchange = await self.channel.declare_exchange(name=self.exchange_name, type='direct')
        queue = await self.channel.declare_queue(name=self.queue_name)

        await queue.bind(exchange=exchange, routing_key=self.routing_key)

        await queue.consume(self.process_message)

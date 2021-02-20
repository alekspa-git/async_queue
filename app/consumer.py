import asyncio
import logging

import aioamqp
import requests

from app.utils import get_config, ConnectorMQ


logging.basicConfig(**{'handlers': (logging.StreamHandler(),)})
logger = logging.getLogger('Consumer')
logger.setLevel(level=logging.INFO)


class ConsumerMQ:
    def __init__(self, config):
        self.config = config
        self.logger = logger

    async def run(self):
        connector = ConnectorMQ(self.logger)
        await connector.connect()

        while True:
            channel = await connector.get_channel()
            await channel.queue_declare(queue_name='message_queue', durable=True)
            await channel.basic_consume(self._message_handler)

    async def _message_handler(self, channel, body, envelope, properties):
        for i in range(5):
            url = self.config['consumer']['web_server']
            try:
                resp = requests.get(url)
            except Exception as exc:
                self.logger.exception("Couldn't connect to web-server: {}".format(exc))
                await asyncio.sleep(5)
                continue

            if resp.status_code == 200:
                await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)
                message = f'{body}: successfully handled by {id(self)}'
                self.logger.info(message)
                return
            else:
                await asyncio.sleep(5)
                continue

        message = f'{body}: failed to process by {id(self)}'
        self.logger.warning(message)


async def main_consumer(count):
    config = get_config()
    aws = []
    for _ in range(count):
        consumer = ConsumerMQ(config)
        aws.append(consumer.run())

    await asyncio.gather(*aws)

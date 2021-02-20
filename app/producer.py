from abc import ABC, abstractmethod
import asyncio
import logging

from app.utils import get_config, ConnectorMQ


logging.basicConfig(**{'handlers': (logging.StreamHandler(),)})
logger = logging.getLogger('Producer')
logger.setLevel(level=logging.INFO)


class ProducerMQ(ABC):
    MESSAGE_TIMEOUT = 1

    def __init__(self, config):
        self.config = config
        self.logger = logger
        self._message_counter = 1

    @abstractmethod
    def generate_message(self):
        pass

    async def run(self):
        connector = ConnectorMQ(self.logger)
        await connector.connect()

        while True:
            channel = await connector.get_channel()
            await channel.queue_declare(queue_name='message_queue', durable=True)
            message = self.generate_message()
            await channel.publish(
                message,
                exchange_name='',
                routing_key='message_queue',
                properties={'delivery_mode': 2}
            )
            message = f'{message}: sent by {id(self)}'
            self.logger.info(message)
            self._message_counter += 1

            await connector.disconnect()
            await asyncio.sleep(self.MESSAGE_TIMEOUT)


class ProducerA(ProducerMQ):
    def generate_message(self):
        return f'ProducerA message #{self._message_counter}'


class ProducerB(ProducerMQ):
    def generate_message(self):
        return f'ProducerB message #{self._message_counter}'


async def main_producer():
    config = get_config()
    producer_a = ProducerA(config)
    producer_b = ProducerB(config)

    await asyncio.gather(
        producer_a.run(),
        producer_b.run()
    )

import asyncio
import os

import aioamqp
import yaml


def get_config():
    path = os.path.join(os.getcwd(), 'app', 'config.yaml')
    with open(path) as f:
        return yaml.safe_load(f)


class ConnectorMQ:
    CONNECTION_TIMEOUT = 10

    def __init__(self, logger):
        self._logger = logger
        self._connection_settings = get_config()['rabbitmq']['connection']
        self._transport = None
        self._protocol = None
        self._channel = None

    async def connect(self):
        while True:
            try:
                transport, protocol = await aioamqp.connect(**self._connection_settings)
            except (ConnectionRefusedError, ConnectionResetError, aioamqp.AmqpClosedConnection) as exc:
                self._logger.warning(f'Connection error: {exc}')
                await asyncio.sleep(self.CONNECTION_TIMEOUT)
            except Exception as exc:
                self._logger.exception(f'Unknown connection error: {exc}')
                raise
            else:
                self._transport = transport
                self._protocol = protocol
                self._channel = await protocol.channel()
                break

    async def disconnect(self):
        await self._protocol.close()
        self._transport.close()
        self._transport = None
        self._protocol = None
        self._channel = None

    async def get_channel(self):
        if not self._channel:
            await self.connect()
        elif not self._channel.is_open:
            await self._channel.open()

        await self._channel.basic_qos(prefetch_count=1, prefetch_size=0, connection_global=False)

        return self._channel

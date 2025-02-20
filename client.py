import asyncio
from random import randint
import logging.config
from logging_config import dict_config
from datetime import datetime


logging.config.dictConfig(dict_config)
client_logger = logging.getLogger('client_logger')


class Client:
    def __init__(self, host, port, client_id):
        self.host = host
        self.port = port
        self.client_id = client_id

    async def connect_to_server(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        try:
            count = 0
            while True:
                interval = randint(300, 3000) / 1000
                await asyncio.sleep(interval)

                message = f'[{count}] PING {self.client_id}'

                response_time = datetime.now()
                response_message = message

                print(f'sending: {message}')
                writer.write(message.encode())
                await writer.drain()

                data = await reader.read(100)

                request_time = datetime.now()
                request_message = data.decode()
                logger_message = f'{response_time} ; {response_message} ; {request_time} ; {request_message}'
                logger_message_2 = f'() ; () ; {request_time} ; {request_message}'

                if data.split()[1] != b'keepalive':
                    client_logger.info(logger_message)

                if data.split()[1] == b'keepalive':
                    client_logger.info(logger_message_2)


                print(f"Received: {data.decode()}")

                count += 1
        except ConnectionError as e:
            print(f'Connection error: {e}')

        finally:
            writer.close()
            await writer.wait_closed()


host = '127.0.0.1'
port = 8888


async def main1():
    client1 = Client(host, port, 1)
    await client1.connect_to_server()


async def main2():
    client2 = Client(host, port, 2)
    await client2.connect_to_server()


async def main():
    await asyncio.gather(main1(), main2())

if __name__ == '__main__':
    asyncio.run(main())
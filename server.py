import asyncio
import datetime
from random import randint
import logging.config
from logging_config import dict_config
from datetime import datetime

logging.config.dictConfig(dict_config)
server_logger = logging.getLogger('server_logger')

connections = []
connections_id = {}
count = 0


async def handle_client(reader, writer, count=count):
    addr = writer.get_extra_info('peername')
    print(f"New connection from {addr}")
    connections.append(writer)
    client_id = None
    while True:
        try:
            data = await reader.read(100)

            if not data:
                break
            message = data.decode()
            parts_message = message.split()
            if len(parts_message) >= 3 and parts_message[2].isdigit:
                client_id = parts_message[2]

            connections_id[client_id] = writer

            request_time = datetime.now()
            request_message = message

            message = f"[{count}/{data.decode()[1]}] PONG ({client_id})"
            print(f"Received: {message}")

            if client_id in connections_id:
                probability = randint(1, 100)
                if probability >= 11:
                    interval = randint(100, 1000) / 1000
                    await asyncio.sleep(interval)
                    connection = connections_id[client_id]
                    connection.write(bytes(message, 'utf-8'))

                    response_time = datetime.now()
                    response_message = message

                    logger_message = f'{request_time}; {request_message}; {response_time}; {response_message}'

                    server_logger.info(logger_message)

                    await connection.drain()
                    count += 1

                if probability <= 10:
                    logger_message_2 = f'{request_time}; {request_message}; (проигнорировано) ; (проигнорировано)'
                    server_logger.info(logger_message_2)




        except Exception as e:
            print(f"Error: {e}")
            break

    if client_id in connections_id:
        connections_id.pop(client_id, None)
    writer.close()
    connections.remove(writer)
    print(f"Connection with {addr} closed")


async def send_keepalive():
    while True:
        for client_id, writer in connections_id.copy().items():
            try:
                writer.write(bytes(f"[{count}] keepalive", 'utf-8'))
                await writer.drain()
            except ConnectionError:
                print(f"Connection with {client_id} closed")
                connections_id.pop(client_id, None)
        await asyncio.sleep(5)


async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    asyncio.create_task(send_keepalive())

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
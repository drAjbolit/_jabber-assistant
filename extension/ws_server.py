import asyncio
import json
import threading

import websockets


class WSServer:

    def __init__(self):

        self.queue = []

    async def handler(
        self,
        websocket
    ):

        async for message in websocket:

            try:

                data = json.loads(
                    message
                )

                self.queue.append(
                    data
                )

            except Exception as e:

                print(
                    "WS ERROR:",
                    e
                )

    async def run_server(self):

        server = await websockets.serve(
            self.handler,
            "127.0.0.1",
            8765
        )

        await server.wait_closed()

    def start(self):

        def worker():

            asyncio.run(
                self.run_server()
            )

        threading.Thread(
            target=worker,
            daemon=True
        ).start()

    def get_events(self):

        events = self.queue[:]

        self.queue.clear()

        return events
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

        print(
            "[WS CLIENT CONNECTED]"
        )

        try:

            async for message in websocket:

                try:

                    data = json.loads(
                        message
                    )

                    if (
                        data.get("type")
                        == "heartbeat"
                    ):
                        continue

                    print(
                        "[WS]",
                        data
                    )

                    self.queue.append(
                        data
                    )

                except Exception as e:

                    print(
                        "WS PARSE ERROR:",
                        e
                    )

        except Exception as e:

            print(
                "[WS CONNECTION ERROR]",
                repr(e)
            )

        finally:

            print(
                "[WS CLIENT DISCONNECTED]"
            )

    async def run_server(
        self
    ):

        server = await websockets.serve(
            self.handler,
            "127.0.0.1",
            8765
        )

        print(
            "WS STARTED"
        )

        await server.wait_closed()

    def start(
        self
    ):

        threading.Thread(
            target=lambda:
                asyncio.run(
                    self.run_server()
                ),
            daemon=True
        ).start()

    def get_events(
        self
    ):

        events = self.queue[:]

        self.queue.clear()

        return events
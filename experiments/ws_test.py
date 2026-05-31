from assistant.ws_server import WSServer
import time

ws = WSServer()
ws.start()

print("WS STARTED")

while True:

    events = ws.get_events()

    for e in events:
        print(e)

    time.sleep(0.1)
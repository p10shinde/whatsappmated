import asyncio
import websockets
import uuid

mac_id = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
for ele in range(0,8*6,8)][::-1])


async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")
    await websocket.send(mac_id)
    print(f"> {mac_id}")

start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
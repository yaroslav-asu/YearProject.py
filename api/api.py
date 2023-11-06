import asyncio
import typing
from typing import Dict, Tuple

from fastapi import FastAPI
from starlette.endpoints import WebSocket, WebSocketEndpoint

UDP_PORT = 8001

app = FastAPI()
ws_clients: Dict[str, WebSocket] = {}


async def send_info_to_client(ws_client: WebSocket, data: bytes) -> None:
    await ws_client.send_json({"recevied": str(data), "from": ws_client.client.host})


class MyUDPProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        self.transport = transport

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        ws_client = ws_clients[addr[0]]
        asyncio.create_task(send_info_to_client(ws_client, data))


@app.websocket_route("/ws-route")
class MyWSEndpoint(WebSocketEndpoint):
    async def on_connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        ws_clients[websocket.client.host] = websocket

        await websocket.send_json({"Msg": "hello world"})

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        ws_clients.pop(websocket.client.host)

    async def on_receive(self, websocket: WebSocket, data: typing.Any) -> None:
        print(data)


@app.on_event("startup")
async def on_startup() -> None:
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: MyUDPProtocol(), local_addr=("0.0.0.0", UDP_PORT)
    )
    app.state.udp_transport = transport
    app.state.udp_protocol = protocol


@app.on_event("shutdown")
async def on_shutdown() -> None:
    app.state.udp_transport.close()

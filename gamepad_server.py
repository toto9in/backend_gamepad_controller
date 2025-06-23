import vgamepad as vg
import asyncio
import websockets
import threading

class GamepadServer:
    def __init__(self):
        self.websocket_server = None
        self.running = False
        self.port = 12345
        self.gamepad = vg.VX360Gamepad()
        self.connections = set()

        self.current_button_states = {
            "r": False,
            "l": False,
            "select": False,
            "start": False,
            "up": False,
            "down": False,
            "right": False,
            "left": False,
            "a": False,
            "b": False,
            "x": False,
            "y": False,
        }

    async def websocket_handler(self, websocket):
        client_info = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        print(f"Tentativa de conexão de {websocket.remote_address}")

        self.connections.add(websocket)

        try:
            async for message in websocket:
                try:
                    self.funcao_mapear
                except Exception as e:
                    print(f"Erro ao processar comando: {e}")
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connections.remove(websocket)


    async def start_websocket_server(self):
        self.websocket_server = await websockets.serve(
            self.websocket_handler, "0.0.0.0", self.port
        )

        await self.websocket_server.wait_closed()


    def start_server(self):
        if self.running:
            return

        self.running = True

        ## i have to initialize another thread to run the websocket server

        def run_async_server():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

            self.server_task = self.loop.create_task(self.start_websocket_server())

            try:
                self.loop.run_forever()
            finally:
                self.loop.close()

        threading.Thread(target=run_async_server).start()

    def stop_server(self):
        if not self.running:
            return

        self.running = False

        if self.websocket_server and self.loop:
            self.loop.call_soon_threadsafe(self.websocket_server.close)

        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)


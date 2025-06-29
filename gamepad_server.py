import vgamepad as vg
import asyncio
import websockets
import threading
import json

class GamepadServer:
    def __init__(self):
        self.websocket_server = None
        self.running = False
        self.port = 12345
        self.gamepad = vg.VX360Gamepad()
        self.connections = set()
        self.loop = None

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

        self.button_mapping = {
            "r": vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
            "l": vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
            "select": vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
            "start": vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
            "up": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
            "down": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
            "right": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
            "left": vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
            "a": vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
            "b": vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
            "x": vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
            "y": vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
        }

    async def websocket_handler(self, websocket):
        client_info = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        print(f"Tentativa de conexão de {websocket.remote_address}")

        self.connections.add(websocket)
        print(f"Cliente conectado: {client_info}")

        try:
            async for message in websocket:
                try:
                    self._map_messages_to_command(message)
                except Exception as e:
                    print(f"Erro ao processar comando: {e}")
        except websockets.exceptions.ConnectionClosed:
            print(f"Conexão fechada: {client_info}")
        finally:
            self.connections.remove(websocket)
            print(f"Cliente desconectado: {client_info}")

    async def start_websocket_server(self):
        self.websocket_server = await websockets.serve(
            self.websocket_handler, "0.0.0.0", self.port
        )
        print(f"Servidor WebSocket iniciado na porta {self.port}")
        await self.websocket_server.wait_closed()

    def start_server(self):
        if self.running:
            return

        self.running = True

        def run_async_server():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

            self.server_task = self.loop.create_task(self.start_websocket_server())

            try:
                self.loop.run_forever()
            finally:
                self.loop.close()


        threading.Thread(target=run_async_server, daemon=True).start()

    def stop_server(self):
        if not self.running:
            return

        self.running = False

        if self.connections and self.loop:
            for ws in self.connections.copy():
                self.loop.call_soon_threadsafe(lambda w=ws: w.close())

        if self.websocket_server and self.loop:
            self.loop.call_soon_threadsafe(self.websocket_server.close)

        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)

    def _map_messages_to_command(self, message_data):
        try:
            cmd_data = json.loads(message_data)


            if "message" in cmd_data:
                message = cmd_data["message"]


                for button_name, is_pressed in message.items():

                    if (button_name in self.current_button_states and
                            self.current_button_states[button_name] != is_pressed):


                        self.current_button_states[button_name] = is_pressed

                        if button_name in self.button_mapping:
                            if is_pressed:
                                self.gamepad.press_button(self.button_mapping[button_name])
                            else:
                                self.gamepad.release_button(self.button_mapping[button_name])


                self.gamepad.update()
            else:
                print(f"Formato de mensagem não reconhecido: {message_data}")

        except json.JSONDecodeError:
            print(f"Erro ao decodificar JSON: {message_data}")
        except Exception as e:
            print(f"Erro ao processar mensagem: {e}")
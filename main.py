import flet as ft
import socket
import qrcode
import io
import base64
from gamepad_server import GamepadServer


class GamepadEmulatorApp:
    def __init__(self):
        self.server = None
        self.connect_button = None
        self.qr_image = None

    def main(self, page: ft.Page):
        page.title = "Gamepad Emulator"
        page.window_width = 400
        page.window_height = 600
        page.window_resizable = False
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.START

        title = ft.Text(
            "Gamepad Emulator",
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        self.connect_button = ft.ElevatedButton("Conectar", width=200, height=50, on_click=self.generate_server_qr_code)

        self.status_text = ft.Text(
            "Pressione conectar para iniciar",
            size=14,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.GREY_700,
        )

        self.qr_image = ft.Image(
            width=250, height=250, fit=ft.ImageFit.CONTAIN, visible=False
        )

        self.instructions = ft.Text(
            "Escaneie o QR Code com seu dispositivo móvel para conectar",
            size=12,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.GREY_600,
            visible=False,
        )

        page.add(
            ft.Container(height=20),
            title,
            ft.Container(height=20),
            self.connect_button,
            ft.Container(height=20),
            self.status_text,
            ft.Container(height=30),
            self.qr_image,
            ft.Container(height=10),
            self.instructions,
        )

        self.page = page

    def generate_server_qr_code(self, e):
        if self.server is None:
            self.start_server()
        else:
            self.stop_server()

    def start_server(self):
        self.server = GamepadServer()
        self.server.start_server()
        ## start server, i need to create the server class and methods

        ## todo generate qr code with server port
        local_ip = self.get_local_ip()
        connection_info = f"ws://{local_ip}:{self.server.port}"

        self.generate_qr_code(connection_info)

        self.connect_button.text = "Desconectar"
        self.connect_button.bgcolor = ft.Colors.RED_400
        self.qr_image.visible = True
        self.instructions.visible = True
        self.page.update()

    def stop_server(self):
        if self.server:
            self.server.stop_server()
            self.server = None

        self.connect_button.text = "Conectar"
        self.connect_button_bgcolor = None
        self.qr_image.visible = False
        self.instructions.visible = False
        self.page.update()



    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"


    def generate_qr_code(self, data):
        try:
            qr = qrcode.QRCode(version=1,  error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,)
            qr.add_data(data)
            qr.make(fit=True)

            qr_img = qr.make_image(fill_color="black", back_color="white")

            buffer = io.BytesIO()
            qr_img.save(buffer, format="PNG")
            buffer.seek(0)

            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            self.qr_image.src_base64 = img_base64

        except Exception as e:
            self.update_status(f"Erro ao gerar QR Code: {e}")

def main():
    app = GamepadEmulatorApp()
    ft.app(target=app.main)


if __name__ == "__main__":
    main()

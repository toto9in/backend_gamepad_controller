import flet as ft
import socket
import qrcode
import io
import base64
import asyncio
from gamepad_server import GamepadServer


class GamepadEmulatorApp:
    def __init__(self):
        self.server = GamepadServer()
        self.server.start_server()
        print("Servidor iniciado automaticamente")

        self.connect_button = None
        self.qr_image = None
        self.status_text = None
        self.instructions = None
        self.page = None

    def main(self, page: ft.Page):
        page.fonts = {
            "Pixelify": "/fonts/PixelifySans-Medium.ttf"
        }
        page.title = "Gamepad Emulator"
        page.window_width = 400
        page.window_height = 800
        page.window_resizable = False
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.theme = ft.Theme(
            font_family="Pixelify"
        )

        title = ft.Text(
            "Gamepad Emulator",
            size=48,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        gamepad_image = ft.Image(
            src="/images/gamepad2.jpg",
            width=300,
            height=180,
            fit=ft.ImageFit.CONTAIN,
        )

        self.connect_button = ft.ElevatedButton(
            "Mostrar QR Code",
            width=250,
            height=60,
            on_click=self.toggle_qr_code,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20
            ),
        )

        self.status_text = ft.Text(
            "Servidor iniciado, esperando por conexões...",
            size=18,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.GREY_700,
        )

        self.qr_image = ft.Image(
            width=250,
            height=250,
            fit=ft.ImageFit.CONTAIN,
            visible=False,
            src_base64=""
        )

        self.instructions = ft.Text(
            "Escaneie o QR Code com seu dispositivo móvel para conectar",
            size=16,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.GREY_600,
            visible=False,
        )

        page.add(
            title,
            gamepad_image,
            ft.Container(height=5),
            self.connect_button,
            self.status_text,
            self.qr_image,
            self.instructions,
        )

        self.page = page
        page.window_event = self.on_window_event

    def on_window_event(self, e):
        if e.data == "resize":
            self.page.window_event = None
            self.page.set_timer(500, self.generate_qr_code_data)

    def toggle_qr_code(self, e):
        if hasattr(self.qr_image, 'src_base64') and self.qr_image.src_base64:
            self.qr_image.visible = not self.qr_image.visible
            self.instructions.visible = not self.instructions.visible

            if self.qr_image.visible:
                self.connect_button.text = "Ocultar QR Code"
            else:
                self.connect_button.text = "Mostrar QR Code"
        else:
            self.connect_button.text = "Gerando QR Code..."
            self.connect_button.disabled = True
            self.page.update()
            self.generate_qr_code_data()
            self.qr_image.visible = True
            self.instructions.visible = True
            self.connect_button.text = "Ocultar QR Code"
            self.connect_button.disabled = False

        self.page.update()

    def generate_qr_code_data(self, *args):
        try:
            local_ip = self.get_local_ip()
            connection_info = f"ws://{local_ip}:{self.server.port}"
            self.generate_qr_code(connection_info)
        except Exception as e:
            print(f"Error in generate_qr_code_data: {e}")
            self.status_text.value = f"Erro ao gerar dados do QR Code: {e}"
            self.page.update()

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            print(f"Error getting IP: {e}")
            return "localhost"

    def generate_qr_code(self, data):
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            qr_img = qr.make_image(fill_color="black", back_color="white")

            buffer = io.BytesIO()
            qr_img.save(buffer)
            buffer.seek(0)

            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            self.qr_image.src_base64 = img_base64

            if self.page:
                self.page.update()

        except Exception as e:
            print(f"Error generating QR code: {e}")
            if hasattr(self, 'status_text') and self.status_text:
                self.status_text.value = f"Erro ao gerar QR Code: {e}"
                if self.page:
                    self.page.update()

def main():
    app = GamepadEmulatorApp()
    ft.app(target=app.main, assets_dir="assets")


if __name__ == "__main__":
    main()
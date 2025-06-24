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

        self.connect_button = ft.ElevatedButton(
            "Mostrar QR Code",
            width=200,
            height=50,
            on_click=self.toggle_qr_code
        )

        self.status_text = ft.Text(
            "Servidor iniciado, esperando por conexões...",
            size=14,
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
    ft.app(target=app.main)


if __name__ == "__main__":
    main()
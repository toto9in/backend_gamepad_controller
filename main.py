import flet as ft


class GamepadEmulatorApp:
    def __init__(self):
        self.server = None
        self.connect_button = None

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

        self.connect_button = ft.ElevatedButton("Conectar", width=200, height=50)

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


def main():
    app = GamepadEmulatorApp()
    ft.app(target=app.main)


if __name__ == "__main__":
    main()

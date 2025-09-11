from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit
from prompt_toolkit.widgets import Button, Dialog, Label

def main():
    kb = KeyBindings()

    @kb.add("c-c")
    def _(event):
        event.app.exit()

    # Обработчики кнопок
    def on_click(name):
        print(f"Нажата {name}")
        app.exit()

    # Кнопки
    buttons = [
        Button(text="Кнопка 1", handler=lambda: on_click("Кнопка 1")),
        Button(text="Кнопка 2", handler=lambda: on_click("Кнопка 2")),
        Button(text="Кнопка 3", handler=lambda: on_click("Кнопка 3")),
    ]

    # Вертикальная компоновка кнопок
    body = HSplit(buttons, padding=1)

    # Диалог
    dialog = Dialog(
        title="Меню",
        body=body,
        buttons=[],   # нижняя стандартная панель кнопок не нужна
        with_background=True,
    )

    layout = Layout(dialog)

    app = Application(
        layout=layout,
        key_bindings=kb,
        full_screen=True,
    )
    app.run()

if __name__ == "__main__":
    main()

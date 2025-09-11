from prompt_toolkit.shortcuts import button_dialog

def choose_with_buttons(title, text, options):
    """
    options: список строк (названия кнопок)
    возвращает выбранную строку или None
    """
    result = button_dialog(
        title=title,
        text=text,
        buttons=[(opt, opt) for opt in options],  # (value, label)
    ).run()
    return result

if __name__ == "__main__":
    items = ["Да", "Нет", "Отмена"]
    choice = choose_with_buttons("Подтверждение", "Вы уверены?", items)
    print("Вы выбрали:", choice)

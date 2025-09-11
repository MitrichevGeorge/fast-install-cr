from prompt_toolkit.shortcuts import radiolist_dialog

def choose(title, options):
    # options — список строк; преобразуем в пары (value, label)
    values = [(i, opt) for i, opt in enumerate(options)]
    result = radiolist_dialog(
        title=title,
        text="Используйте ↑/↓ и Enter для выбора:",
        values=values,
    ).run()
    return result

if __name__ == "__main__":
    items = ["Первый", "Второй", "Третий", "Выход"]
    idx = choose("Меню", items)
    if idx is None:
        print("Отменено.")
    else:
        print(f"Вы выбрали: {items[idx]} (index={idx})")



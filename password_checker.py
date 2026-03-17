import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import string
import os


LOG_FILE = "log.txt"


def check_password(password):
    score = 0
    comments = []

    if len(password) >= 8:
        score += 1
    else:
        comments.append("пароль короче 8 символов")

    if any(char.islower() for char in password):
        score += 1
    else:
        comments.append("нет строчных букв")

    if any(char.isupper() for char in password):
        score += 1
    else:
        comments.append("нет заглавных букв")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        comments.append("нет цифр")

    if any(char in string.punctuation for char in password):
        score += 1
    else:
        comments.append("нет специальных символов")

    if score <= 2:
        return "Слабый пароль", comments
    elif score <= 4:
        return "Средний пароль", comments
    else:
        return "Надёжный пароль", comments


def save_result(password, result, comments):
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"{now} | Пароль: {password} | Результат: {result}")
        if comments:
            file.write(f" | Замечания: {', '.join(comments)}")
        file.write("\n")


def run_check():
    password = entry_password.get().strip()

    if not password:
        messagebox.showwarning("Предупреждение", "Введите пароль.")
        return

    result, comments = check_password(password)

    if result == "Слабый пароль":
        text_result.config(
            text=(
                "Результат: Слабый пароль\n"
                "Введите более надёжный пароль."
            )
        )
        messagebox.warning(
            "Слабый пароль",
            "Пароль слишком простой.\n"
            "Попробуйте придумать более надёжный пароль."
        )
        entry_password.delete(0, "end")
        entry_password.focus()
        save_result(password, result, comments)
        return

    if result == "Средний пароль":
        text_result.config(
            text=(
                f"Результат: {result}\n"
                f"Недочёты: {', '.join(comments)}"
            )
        )
        save_result(password, result, comments)
        return

    text_result.config(
        text="Результат: Надёжный пароль\nПароль соответствует требованиям."
    )
    save_result(password, result, comments)


def clear_fields():
    entry_password.delete(0, "end")
    text_result.config(text="Здесь будет результат проверки")
    entry_password.focus()


def open_help():
    help_window = tk.Toplevel(root)
    help_window.title("Справка")
    help_window.geometry("420x260")
    help_window.resizable(False, False)

    help_text = (
        "Требования к надёжному паролю:\n\n"
        "1. Минимум 8 символов\n"
        "2. Наличие строчных букв\n"
        "3. Наличие заглавных букв\n"
        "4. Наличие цифр\n"
        "5. Наличие специальных символов\n\n"
        "Пример надёжного пароля:\n"
        "Qwerty123!"
    )

    label_help = tk.Label(
        help_window,
        text=help_text,
        font=("Arial", 12),
        justify="left",
        anchor="w"
    )
    label_help.pack(padx=15, pady=15, fill="both")


def open_history():
    history_window = tk.Toplevel(root)
    history_window.title("История проверок")
    history_window.geometry("700x400")

    text_history = tk.Text(history_window, font=("Arial", 11), wrap="word")
    text_history.pack(expand=True, fill="both", padx=10, pady=10)

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            content = file.read()
            if content.strip():
                text_history.insert("1.0", content)
            else:
                text_history.insert("1.0", "История пока пуста.")
    else:
        text_history.insert("1.0", "Файл log.txt ещё не создан.")

    text_history.config(state="disabled")


root = tk.Tk()
root.title("Password Checker")
root.geometry("560x420")
root.resizable(False, False)

label_title = tk.Label(
    root,
    text="Проверка надёжности пароля",
    font=("Arial", 16, "bold")
)
label_title.pack(pady=15)

label_password = tk.Label(
    root,
    text="Введите пароль:",
    font=("Arial", 12)
)
label_password.pack()

entry_password = tk.Entry(
    root,
    width=32,
    font=("Arial", 12),
    show="*"
)
entry_password.pack(pady=10)

button_check = tk.Button(
    root,
    text="Проверить пароль",
    font=("Arial", 12),
    width=20,
    command=run_check
)
button_check.pack(pady=5)

button_clear = tk.Button(
    root,
    text="Очистить",
    font=("Arial", 12),
    width=20,
    command=clear_fields
)
button_clear.pack(pady=5)

button_help = tk.Button(
    root,
    text="Справка",
    font=("Arial", 12),
    width=20,
    command=open_help
)
button_help.pack(pady=5)

button_history = tk.Button(
    root,
    text="История",
    font=("Arial", 12),
    width=20,
    command=open_history
)
button_history.pack(pady=5)

text_result = tk.Label(
    root,
    text="Здесь будет результат проверки",
    font=("Arial", 11),
    wraplength=500,
    justify="left"
)
text_result.pack(pady=20)

root.mainloop()
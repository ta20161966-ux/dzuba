import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.history = self.load_history()
        self.create_widgets()
        self.update_history_table()

    def create_widgets(self):
        # Длина пароля
        tk.Label(self.root, text="Длина пароля:").grid(row=0, column=0, padx=5, pady=5)
        self.length_scale = tk.Scale(self.root, from_=6, to=32, orient=tk.HORIZONTAL)
        self.length_scale.grid(row=0, column=1, padx=5, pady=5)

        # Чекбоксы
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)

        tk.Checkbutton(self.root, text="Цифры", variable=self.use_digits).grid(row=1, column=0, sticky='w')
        tk.Checkbutton(self.root, text="Буквы", variable=self.use_letters).grid(row=2, column=0, sticky='w')
        tk.Checkbutton(self.root, text="Верхний регистр", variable=self.use_upper).grid(row=3, column=0, sticky='w')
        tk.Checkbutton(self.root, text="Спецсимволы", variable=self.use_special).grid(row=4, column=0, sticky='w')

        # Кнопка генерации
        tk.Button(self.root, text="Сгенерировать", command=self.generate_password).grid(row=5, column=0, columnspan=2, pady=10)

        # Поле вывода пароля
        self.password_entry = tk.Entry(self.root, width=40)
        self.password_entry.grid(row=6, column=0, columnspan=2, pady=5)

        # Таблица истории
        self.history_tree = ttk.Treeview(self.root, columns=("password",), show="headings")
        self.history_tree.heading("password", text="История паролей")
        self.history_tree.grid(row=7, column=0, columnspan=2, pady=10)

    def generate_password(self):
        length = self.length_scale.get()
        chars = ''
        if self.use_digits.get():
            chars += string.digits
        if self.use_letters.get():
            chars += string.ascii_lowercase
            if self.use_upper.get():
                chars += string.ascii_uppercase
        if self.use_special.get():
            chars += string.punctuation

        if not chars:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
            return

        password = ''.join(random.choices(chars, k=length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

        self.history.append(password)
        self.save_history()
        self.update_history_table()

    def save_history(self):
        with open('history.json', 'w') as f:
            json.dump(self.history, f)

    def load_history(self):
        try:
            with open('history.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def update_history_table(self):
        for i in self.history_tree.get_children():
            self.history_tree.delete(i)
        for pwd in self.history:
            self.history_tree.insert("", "end", values=(pwd,))

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

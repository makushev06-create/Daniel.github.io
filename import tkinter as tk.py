import tkinter as tk
from tkinter import scrolledtext
import tkinter.messagebox

class Command:
    """
    Абстрактный класс команды.
    """
    def __init__(self, editor):
        self.editor = editor
        self.backup = ""

    def backup(self):
        """Сохраняет текущее состояние текста."""
        self.backup = self.editor.text_area.get("1.0", tk.END)

    def undo(self):
        """Восстанавливает текст из резервной копии."""
        self.editor.text_area.delete("1.0", tk.END)
        self.editor.text_area.insert("1.0", self.backup)

    def execute(self):
        """Абстрактный метод выполнения команды."""
        raise NotImplementedError


class CopyCommand(Command):
    """Команда копирования."""
    def __init__(self, editor):
        super().__init__(editor)

    def execute(self):
        try:
            selected_text = self.editor.text_area.selection_get()
            self.editor.clipboard = selected_text
            return False  # Копирование не изменяет состояние редактора
        except tk.TclError:
            return False # Нет выделенного текста

class CutCommand(Command):
    """Команда вырезания."""
    def __init__(self, editor):
        super().__init__(editor)

    def execute(self):
        try:
            selected_text = self.editor.text_area.selection_get()
            self.backup()
            self.editor.clipboard = selected_text
            self.editor.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
            return True # Вырезание меняет состояние редактора
        except tk.TclError:
            return False  # Нет выделенного текста

class PasteCommand(Command):
    """Команда вставки."""
    def __init__(self, editor):
        super().__init__(editor)

    def execute(self):
        if not self.editor.clipboard:
            return False
        self.backup()
        self.editor.text_area.insert(tk.INSERT, self.editor.clipboard)
        return True # Вставка меняет состояние редактора


class CommandHistory:
    """История команд для поддержки отмены."""
    def __init__(self):
        self.history = []

    def push(self, command):
        self.history.append(command)

    def pop(self):
        if self.history:
            return self.history.pop()
        return None

    def is_empty(self):
        return not self.history
class Editor:
    """
    Класс текстового редактора.
    """
    def __init__(self, master):
        self.master = master
        master.title("Текстовый редактор (Python Command Pattern)")

        self.text_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH)

        self.clipboard = ""
        self.history = CommandHistory()

        # Создание кнопок
        self.copy_button = tk.Button(master, text="Ctrl+C", command=self.copy_text)
        self.cut_button = tk.Button(master, text="Ctrl+X", command=self.cut_text)
        self.paste_button = tk.Button(master, text="Ctrl+V", command=self.paste_text)
        self.undo_button = tk.Button(master, text="Ctrl+Z", command=self.undo)

        self.copy_button.pack(side=tk.LEFT)
        self.cut_button.pack(side=tk.LEFT)
        self.paste_button.pack(side=tk.LEFT)
        self.undo_button.pack(side=tk.LEFT)

        # Bind keyboard shortcuts (optional)
        master.bind("<Control-c>", lambda event: self.copy_text())
        master.bind("<Control-x>", lambda event: self.cut_text())
        master.bind("<Control-v>", lambda event: self.paste_text())
        master.bind("<Control-z>", lambda event: self.undo())

    def copy_text(self):
        """Выполняет команду копирования."""
        command = CopyCommand(self)
        self.execute_command(command)

    def cut_text(self):
        """Выполняет команду вырезания."""
        command = CutCommand(self)
        self.execute_command(command)

    def paste_text(self):
        """Выполняет команду вставки."""
        command = PasteCommand(self)
        self.execute_command(command)

    def execute_command(self, command):
        """Выполняет команду и добавляет ее в историю."""
        if command.execute():
            self.history.push(command)

    def undo(self):
        """Отменяет последнюю выполненную команду."""
        if self.history.is_empty():
            return

        command = self.history.pop()
        if command:
            command.undo()

# Клиентский код:
if __name__ == "__main__":
    root = tk.Tk()
    editor = Editor(root)
    root.mainloop()

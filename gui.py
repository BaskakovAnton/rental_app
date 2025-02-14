import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database as db
from bikes_tab import BikesTab
from customers_tab import CustomersTab
# from rentals_tab import RentalsTab  # TODO: Создать
# from summary_tab import SummaryTab  # TODO: Создать

class RentalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение для управления прокатом велотехники")

        self.conn = db.create_connection()
        # Ensure tables are created
        if self.conn:
            db.create_tables(self.conn)
        else:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            root.destroy()
            return

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Создание вкладок
        self.bikes_tab = ttk.Frame(self.notebook)
        self.customers_tab = ttk.Frame(self.notebook)
        self.rentals_tab = ttk.Frame(self.notebook)
        self.summary_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.bikes_tab, text="Велосипеды")
        self.notebook.add(self.customers_tab, text="Клиенты")
        self.notebook.add(self.rentals_tab, text="Аренда")
        self.notebook.add(self.summary_tab, text="Отчетность")

        # Инициализация вкладок
        self.bikes_tab_instance = BikesTab(self, self.bikes_tab)  # Pass self (RentalApp instance)
        self.customers_tab_instance = CustomersTab(self, self.customers_tab)  # Pass self
        # self.rentals_tab_instance = RentalsTab(self, self.rentals_tab)  # TODO: Создать
        # self.summary_tab_instance = SummaryTab(self, self.summary_tab)  # TODO: Создать

        # Кнопка "Выход"
        exit_button = ttk.Button(self.root, text="Выход", command=self.close)
        exit_button.pack(pady=10)

    def close(self):
        db.close_connection(self.conn)
        self.root.destroy()

    def __del__(self):
        pass

if __name__ == '__main__':
    root = tk.Tk()
    app = RentalApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database as db
import re  # Для валидации email

class RentalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение для управления прокатом велотехники")

        self.conn = db.create_connection()
        # Ensure tables are created
        if self.conn:
            db.create_tables(self.conn)  # ADD THIS LINE
        else:
            messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.")
            root.destroy()  # Закрываем приложение, если не удалось подключиться к БД
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
        self.init_bikes_tab()
        self.init_customers_tab()  # ADD THIS LINE
        # self.init_rentals_tab()    # TODO: Создать
        # self.init_summary_tab()    # TODO: Создать

        # Кнопка "Выход"
        exit_button = ttk.Button(self.root, text="Выход", command=self.close)
        exit_button.pack(pady=10)

    def init_bikes_tab(self):
        # (Код для вкладки "Велосипеды" - без изменений)
        # ... (Ваш существующий код для init_bikes_tab)
        pass  # Заглушка, чтобы не было ошибок, пока не скопируете свой код

    def init_customers_tab(self):
        """Создает интерфейс вкладки 'Клиенты'."""

        # Переменные для хранения данных о клиентах
        self.customer_name_var = tk.StringVar()
        self.phone_number_var = tk.StringVar()
        self.email_var = tk.StringVar()

        # Фрейм для ввода данных о клиенте
        customer_input_frame = ttk.LabelFrame(self.customers_tab, text="Информация о клиенте")
        customer_input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Метки и поля ввода
        ttk.Label(customer_input_frame, text="Имя:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(customer_input_frame, textvariable=self.customer_name_var).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(customer_input_frame, text="Телефон:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(customer_input_frame, textvariable=self.phone_number_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(customer_input_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(customer_input_frame, textvariable=self.email_var).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Кнопки
        customer_button_frame = ttk.Frame(self.customers_tab)
        customer_button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(customer_button_frame, text="Добавить", command=self.add_customer).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(customer_button_frame, text="Обновить", command=self.update_customer).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(customer_button_frame, text="Удалить", command=self.delete_customer).grid(row=0, column=2, padx=5, pady=5)

        # Таблица для отображения клиентов
        self.customers_tree = ttk.Treeview(self.customers_tab, columns=("ID", "Имя", "Телефон", "Email"), show="headings")
        self.customers_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Заголовки столбцов
        self.customers_tree.heading("ID", text="ID")
        self.customers_tree.heading("Имя", text="Имя")
        self.customers_tree.heading("Телефон", text="Телефон")
        self.customers_tree.heading("Email", text="Email")

        # Настройка ширины столбцов
        self.customers_tree.column("ID", width=30)
        self.customers_tree.column("Имя", width=150)
        self.customers_tree.column("Телефон", width=100)
        self.customers_tree.column("Email", width=150)

        # Привязка события выбора строки
        self.customers_tree.bind("<ButtonRelease-1>", self.select_customer)

        # Конфигурация сетки для изменения размеров
        self.customers_tab.columnconfigure(0, weight=1)
        self.customers_tab.rowconfigure(2, weight=1)
        customer_input_frame.columnconfigure(1, weight=1)

        # Загрузка данных о клиентах в таблицу
        self.populate_customers_table()

    def add_customer(self):
        """Добавляет нового клиента в базу данных."""
        customer_name = self.customer_name_var.get()
        phone_number = self.phone_number_var.get()
        email = self.email_var.get()

        if not customer_name:
            messagebox.showerror("Ошибка", "Пожалуйста, введите имя клиента.")
            return

        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Ошибка", "Неверный формат email.")
            return

        customer = (customer_name, phone_number, email)
        try:
            customer_id = db.insert_customer(self.conn, customer)
            if customer_id:
                messagebox.showinfo("Успех", "Клиент успешно добавлен.")
                self.populate_customers_table()
                self.clear_customer_inputs()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить клиента.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при добавлении клиента: {e}")

    def update_customer(self):
        """Обновляет информацию о клиенте."""
        selected_item = self.customers_tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите клиента для обновления.")
            return

        customer_id = self.customers_tree.item(selected_item[0])['values'][0]

        customer_name = self.customer_name_var.get()
        phone_number = self.phone_number_var.get()
        email = self.email_var.get()

        if not customer_name:
            messagebox.showerror("Ошибка", "Пожалуйста, введите имя клиента.")
            return

        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Ошибка", "Неверный формат email.")
            return

        customer = (customer_name, phone_number, email)
        try:
            db.update_customer(self.conn, customer_id, customer)
            messagebox.showinfo("Успех", "Информация о клиенте успешно обновлена.")
            self.populate_customers_table()
            self.clear_customer_inputs()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при обновлении клиента: {e}")

    def delete_customer(self):
        """Удаляет клиента из базы данных."""
        selected_item = self.customers_tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите клиента для удаления.")
            return

        customer_id = self.customers_tree.item(selected_item[0])['values'][0]

        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого клиента?"):
            try:
                db.delete_customer(self.conn, customer_id)
                messagebox.showinfo("Успех", "Клиент успешно удален.")
                self.populate_customers_table()
                self.clear_customer_inputs()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Произошла ошибка при удалении клиента: {e}")

    def populate_customers_table(self):
        """Загружает данные о клиентах из базы данных в таблицу."""
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)

        try:
            customers = db.select_all_customers(self.conn)
            for customer in customers:
                self.customers_tree.insert("", tk.END, values=customer)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при загрузке данных о клиентах: {e}")

    def select_customer(self, event):
        """Заполняет поля ввода данными из выбранного клиента."""
        selected_item = self.customers_tree.selection()
        if selected_item:
            customer = self.customers_tree.item(selected_item[0])['values']
            self.customer_name_var.set(customer[1])
            self.phone_number_var.set(customer[2])
            self.email_var.set(customer[3])

    def clear_customer_inputs(self):
        """Очищает поля ввода для клиентов."""
        self.customer_name_var.set("")
        self.phone_number_var.set("")
        self.email_var.set("")

    def close(self):
        db.close_connection(self.conn)
        self.root.destroy()

    def __del__(self):
        pass # prevent error

if __name__ == '__main__':
    root = tk.Tk()
    app = RentalApp(root)
    root.mainloop()
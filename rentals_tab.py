import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database as db
from tkcalendar import DateEntry
import logging

# Настройка логгера
logging.basicConfig(filename='rental_app.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class RentalsTab:
    def __init__(self, parent, container):
        self.parent = parent  # RentalApp instance
        self.container = container  # ttk.Frame for this tab
        self.conn = parent.conn  # Access the database connection

        # Переменные для хранения данных
        self.bike_var = tk.StringVar()
        self.customer_var = tk.StringVar()
        self.rental_fee_var = tk.DoubleVar()

        # Словари для хранения ID велосипедов и клиентов
        self.bikes_data = {}
        self.customers_data = {}

        self.create_widgets()
        self.load_bikes_into_combobox()
        self.load_customers_into_combobox()
        self.populate_rentals_table() # Initial population

    def create_widgets(self):
        rental_input_frame = ttk.LabelFrame(self.container, text="Информация об аренде")
        rental_input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Выбор велосипеда
        ttk.Label(rental_input_frame, text="Велосипед:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.bike_combobox = ttk.Combobox(rental_input_frame, textvariable=self.bike_var, values=[])
        self.bike_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Выбор клиента
        ttk.Label(rental_input_frame, text="Клиент:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.customer_combobox = ttk.Combobox(rental_input_frame, textvariable=self.customer_var, values=[])
        self.customer_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Дата аренды
        ttk.Label(rental_input_frame, text="Дата аренды:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.rental_date_entry = DateEntry(rental_input_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.rental_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Дата возврата
        ttk.Label(rental_input_frame, text="Дата возврата:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.return_date_entry = DateEntry(rental_input_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.return_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Стоимость аренды
        ttk.Label(rental_input_frame, text="Стоимость аренды:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(rental_input_frame, textvariable=self.rental_fee_var).grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Кнопки
        rental_button_frame = ttk.Frame(self.container)
        rental_button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(rental_button_frame, text="Начать аренду", command=self.start_rental).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(rental_button_frame, text="Завершить аренду", command=self.end_rental).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(rental_button_frame, text="Удалить аренду", command=self.delete_rental).grid(row=0, column=2, padx=5, pady=5)

        # Таблица для отображения аренд
        self.rentals_tree = ttk.Treeview(self.container, columns=("ID", "Велосипед", "Клиент", "Дата аренды", "Дата возврата", "Стоимость", "Статус"), show="headings")
        self.rentals_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.rentals_tree.heading("ID", text="ID")
        self.rentals_tree.heading("Велосипед", text="Велосипед")
        self.rentals_tree.heading("Клиент", text="Клиент")
        self.rentals_tree.heading("Дата аренды", text="Дата аренды")
        self.rentals_tree.heading("Дата возврата", text="Дата возврата")
        self.rentals_tree.heading("Стоимость", text="Стоимость")
        self.rentals_tree.heading("Статус", text="Статус")

        self.rentals_tree.column("ID", width=30)
        self.rentals_tree.column("Велосипед", width=100)
        self.rentals_tree.column("Клиент", width=100)
        self.rentals_tree.column("Дата аренды", width=80)
        self.rentals_tree.column("Дата возврата", width=80)
        self.rentals_tree.column("Стоимость", width=60)
        self.rentals_tree.column("Статус", width=80)

        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(2, weight=1)
        rental_input_frame.columnconfigure(1, weight=1)

    def load_bikes_into_combobox(self):
        """Загружает список велосипедов в Combobox."""
        try:
            bikes = db.select_all_bikes(self.conn)
            self.bikes_data = {bike[1]: bike[0] for bike in bikes}  # Словарь: имя велосипеда -> ID
            bike_names = list(self.bikes_data.keys())  # Получаем список имен велосипедов из словаря
            self.bike_combobox['values'] = bike_names
            logging.debug(f"Успешно загружены велосипеды в Combobox: {bike_names}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке велосипедов: {e}")
            logging.exception(f"Ошибка при загрузке велосипедов: {e}")

    def load_customers_into_combobox(self):
        """Загружает список клиентов в Combobox."""
        try:
            customers = db.select_all_customers(self.conn)
            self.customers_data = {customer[1]: customer[0] for customer in customers}  # Словарь: имя клиента -> ID
            customer_names = list(self.customers_data.keys())  # Получаем список имен клиентов из словаря
            self.customer_combobox['values'] = customer_names
            logging.debug(f"Успешно загружены клиенты в Combobox: {customer_names}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке клиентов: {e}")
            logging.exception(f"Ошибка при загрузке клиентов: {e}")

    def start_rental(self):
        """Начинает новую аренду."""
        logging.debug("Вызвана функция start_rental()")  # Log

        try:
            # Получение данных из интерфейса
            bike_name = self.bike_var.get()
            customer_name = self.customer_var.get()
            rental_date = self.rental_date_entry.get_date()
            return_date = self.return_date_entry.get_date()
            rental_fee = self.rental_fee_var.get()

            logging.debug(f"Данные из интерфейса: Велосипед={bike_name}, Клиент={customer_name}, Дата аренды={rental_date}, Дата возврата={return_date}, Стоимость={rental_fee}") # Log

            # Валидация данных (пример)
            if not bike_name or not customer_name or not rental_date or not rental_fee:
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
                logging.warning("Не заполнены все поля.") # Log
                return

            # Получение ID велосипеда и клиента
            bike_id = self.bikes_data.get(bike_name)
            customer_id = self.customers_data.get(customer_name)

            logging.debug(f"ID велосипеда={bike_id}, ID клиента={customer_id}") # Log

            if not bike_id or not customer_id:
                messagebox.showerror("Ошибка", "Неверный велосипед или клиент.")
                logging.error("Неверный велосипед или клиент.") # Log
                return

            # Создание записи об аренде
            rental = (bike_id, customer_id, rental_date, return_date, rental_fee, 'Активно')  # Статус "Активно"
            rental_id = db.insert_rental(self.conn, rental)

            if rental_id:
                messagebox.showinfo("Успех", "Аренда успешно начата.")
                logging.info(f"Аренда успешно начата. ID аренды: {rental_id}") # Log
                self.populate_rentals_table()  # Обновляем таблицу
                self.clear_rental_inputs()  # Очищаем поля ввода
            else:
                messagebox.showerror("Ошибка", "Не удалось начать аренду.")
                logging.error("Не удалось начать аренду.") # Log

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            logging.exception(f"Произошла ошибка: {e}") # Log exception

        logging.debug("Завершение функции start_rental()") # Log

    def end_rental(self):
        """Завершает аренду."""
        logging.debug("Вызвана функция end_rental()")

        try:
            # Получение выбранной аренды
            selected_item = self.rentals_tree.selection()
            if not selected_item:
                messagebox.showerror("Ошибка", "Пожалуйста, выберите аренду для завершения.")
                logging.warning("Не выбрана аренда для завершения.")
                return

            rental_id = self.rentals_tree.item(selected_item[0])['values'][0]
            logging.debug(f"Выбрана аренда с ID: {rental_id}")

            # Подтверждение завершения
            if not messagebox.askyesno("Подтверждение", "Вы уверены, что хотите завершить эту аренду?"):
                logging.info("Завершение аренды отменено пользователем.")
                return

            # Получение даты возврата
            return_date = self.return_date_entry.get_date()
            logging.debug(f"Дата возврата: {return_date}")

            # Обновление статуса аренды в базе данных
            rental = db.select_rental_by_id(self.conn, rental_id)
            if rental:
                bike_id = rental[1]
                customer_id = rental[2]
                rental_date = rental[3]
                rental_fee = rental[5]

                updated_rental = (bike_id, customer_id, rental_date, return_date, rental_fee, 'Завершено')
                db.update_rental(self.conn, rental_id, updated_rental)

                messagebox.showinfo("Успех", "Аренда успешно завершена.")
                logging.info(f"Аренда с ID {rental_id} успешно завершена.")
                self.populate_rentals_table()  # Обновляем таблицу
            else:
                messagebox.showerror("Ошибка", "Не удалось найти аренду с указанным ID.")
                logging.error(f"Не удалось найти аренду с ID {rental_id}.")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            logging.exception(f"Произошла ошибка: {e}")

        logging.debug("Завершение функции end_rental()")

    def delete_rental(self):
        """Удаляет аренду."""
        logging.debug("Вызвана функция delete_rental()")

        try:
            # Получение выбранной аренды
            selected_item = self.rentals_tree.selection()
            if not selected_item:
                messagebox.showerror("Ошибка", "Пожалуйста, выберите аренду для удаления.")
                logging.warning("Не выбрана аренда для удаления.")
                return

            rental_id = self.rentals_tree.item(selected_item[0])['values'][0]
            logging.debug(f"Выбрана аренда с ID: {rental_id}")

            # Подтверждение удаления
            if not messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту аренду?"):
                logging.info("Удаление аренды отменено пользователем.")
                return

            # Удаление аренды из базы данных
            db.delete_rental(self.conn, rental_id)

            messagebox.showinfo("Успех", "Аренда успешно удалена.")
            logging.info(f"Аренда с ID {rental_id} успешно удалена.")
            self.populate_rentals_table()  # Обновляем таблицу

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            logging.exception(f"Произошла ошибка: {e}")

        logging.debug("Завершение функции delete_rental()")

    def populate_rentals_table(self):
        """Загружает данные об арендах из базы данных в таблицу."""
        for item in self.rentals_tree.get_children():
            self.rentals_tree.delete(item)

        try:
            rentals = db.select_all_rentals(self.conn)
            for rental in rentals:
                # Получаем имена велосипеда и клиента по их ID
                bike_id = rental[1]
                customer_id = rental[2]

                bike_name = next((name for name, id in self.bikes_data.items() if id == bike_id), "Неизвестно")
                customer_name = next((name for name, id in self.customers_data.items() if id == customer_id), "Неизвестно")

                # Форматируем дату
                rental_date = rental[3]
                return_date = rental[4]

                self.rentals_tree.insert("", tk.END, values=(rental[0], bike_name, customer_name, rental_date, return_date, rental[5], rental[6]))
            logging.debug("Таблица аренд успешно обновлена.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке данных об арендах: {e}")
            logging.exception(f"Ошибка при загрузке данных об арендах: {e}")

    def clear_rental_inputs(self):
        """Очищает поля ввода для аренды."""
        self.bike_var.set("")
        self.customer_var.set("")
        self.rental_date_entry.set_date(None)  # Очищаем DateEntry
        self.return_date_entry.set_date(None)  # Очищаем DateEntry
        self.rental_fee_var.set(0.0)
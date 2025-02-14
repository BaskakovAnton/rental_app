import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database as db
from tkcalendar import DateEntry
import logging

# Настройка логгера
logging.basicConfig(filename='rental_app.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class SummaryTab:
    def __init__(self, parent, container):
        self.parent = parent
        self.container = container
        self.conn = parent.conn

        self.date_var = tk.StringVar()
        self.total_revenue_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        summary_input_frame = ttk.LabelFrame(self.container, text="Отчетность")
        summary_input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Выбор даты
        ttk.Label(summary_input_frame, text="Выберите дату:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = DateEntry(summary_input_frame, width=12, background='darkblue', foreground='white', borderwidth=2, textvariable=self.date_var)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Кнопка "Получить отчет"
        ttk.Button(summary_input_frame, text="Получить отчет", command=self.generate_report).grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Метка для отображения общей прибыли
        ttk.Label(summary_input_frame, text="Общая прибыль за день:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.total_revenue_label = ttk.Label(summary_input_frame, textvariable=self.total_revenue_var)
        self.total_revenue_label.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    def generate_report(self):
        """Генерирует отчет о прибыли за выбранную дату."""
        logging.debug("Вызвана функция generate_report()")

        try:
            selected_date = self.date_entry.get_date()
            logging.debug(f"Выбрана дата: {selected_date}")

            # Получение общей прибыли из базы данных
            total_revenue = db.get_rental_summary(self.conn, selected_date)
            logging.debug(f"Общая прибыль за день: {total_revenue}")

            # Отображение общей прибыли в метке
            self.total_revenue_var.set(f"{total_revenue} руб.")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            logging.exception(f"Произошла ошибка: {e}")

        logging.debug("Завершение функции generate_report()")
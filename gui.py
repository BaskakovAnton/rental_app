import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database as db

class RentalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение для управления прокатом велотехники")

        self.conn = db.create_connection()
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
        # self.init_customers_tab()  # TODO: Создать
        # self.init_rentals_tab()    # TODO: Создать
        # self.init_summary_tab()    # TODO: Создать

    def init_bikes_tab(self):
        # Переменные для велосипедов
        self.bike_name_var = tk.StringVar()
        self.bike_type_var = tk.StringVar()
        self.bike_size_var = tk.StringVar()
        self.rental_price_var = tk.DoubleVar()
        self.availability_var = tk.IntVar(value=1)

        # Фрейм для ввода данных о велосипедах
        bike_input_frame = ttk.LabelFrame(self.bikes_tab, text="Информация о велосипеде")
        bike_input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(bike_input_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(bike_input_frame, textvariable=self.bike_name_var).grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(bike_input_frame, text="Тип:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(bike_input_frame, textvariable=self.bike_type_var).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(bike_input_frame, text="Размер:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(bike_input_frame, textvariable=self.bike_size_var).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(bike_input_frame, text="Цена аренды:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(bike_input_frame, textvariable=self.rental_price_var).grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(bike_input_frame, text="Доступность:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        available_check = ttk.Checkbutton(bike_input_frame, text="Доступен", variable=self.availability_var)
        available_check.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Кнопки для велосипедов
        bike_button_frame = ttk.Frame(self.bikes_tab)
        bike_button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(bike_button_frame, text="Добавить", command=self.add_bike).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(bike_button_frame, text="Обновить", command=self.update_bike).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(bike_button_frame, text="Удалить", command=self.delete_bike).grid(row=0, column=2, padx=5, pady=5)

        # Таблица для велосипедов
        self.bikes_tree = ttk.Treeview(self.bikes_tab, columns=("ID", "Название", "Тип", "Размер", "Цена", "Доступность"), show="headings")
        self.bikes_tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.bikes_tree.heading("ID", text="ID")
        self.bikes_tree.heading("Название", text="Название")
        self.bikes_tree.heading("Тип", text="Тип")
        self.bikes_tree.heading("Размер", text="Размер")
        self.bikes_tree.heading("Цена", text="Цена")
        self.bikes_tree.heading("Доступность", text="Доступность")

        self.bikes_tree.column("ID", width=30)
        self.bikes_tree.column("Название", width=100)
        self.bikes_tree.column("Тип", width=80)
        self.bikes_tree.column("Размер", width=50)
        self.bikes_tree.column("Цена", width=60)
        self.bikes_tree.column("Доступность", width=80)

        self.bikes_tree.bind("<ButtonRelease-1>", self.select_bike)

        # Загрузка данных в таблицу велосипедов
        self.populate_bikes_table()

        self.bikes_tab.columnconfigure(0, weight=1)
        self.bikes_tab.rowconfigure(2, weight=1)
        bike_input_frame.columnconfigure(1, weight=1)

    def populate_bikes_table(self):
        """Загружает данные о велосипедах из базы данных в таблицу."""
        for item in self.bikes_tree.get_children():
            self.bikes_tree.delete(item)

        bikes = db.select_all_bikes(self.conn)
        for bike in bikes:
            self.bikes_tree.insert("", tk.END, values=bike)

    def add_bike(self):
        """Добавляет новый велосипед в базу данных."""
        bike_name = self.bike_name_var.get()
        bike_type = self.bike_type_var.get()
        bike_size = self.bike_size_var.get()
        rental_price = self.rental_price_var.get()
        availability = self.availability_var.get()

        if not all([bike_name, rental_price]):
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все обязательные поля (Название и Цена).")
            return

        bike = (bike_name, bike_type, bike_size, rental_price, availability)
        bike_id = db.insert_bike(self.conn, bike)

        if bike_id:
            messagebox.showinfo("Успех", "Велосипед успешно добавлен.")
            self.populate_bikes_table()
            self.clear_bike_inputs()
        else:
            messagebox.showerror("Ошибка", "Не удалось добавить велосипед.")

    def update_bike(self):
        """Обновляет информацию о велосипеде."""
        selected_item = self.bikes_tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите велосипед для обновления.")
            return

        bike_id = self.bikes_tree.item(selected_item[0])['values'][0]

        bike_name = self.bike_name_var.get()
        bike_type = self.bike_type_var.get()
        bike_size = self.bike_size_var.get()
        rental_price = self.rental_price_var.get()
        availability = self.availability_var.get()

        if not all([bike_name, rental_price]):
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все обязательные поля (Название и Цена).")
            return

        bike = (bike_name, bike_type, bike_size, rental_price, availability)
        db.update_bike(self.conn, bike_id, bike)
        messagebox.showinfo("Успех", "Информация о велосипеде успешно обновлена.")
        self.populate_bikes_table()
        self.clear_bike_inputs()

    def delete_bike(self):
        """Удаляет велосипед из базы данных."""
        selected_item = self.bikes_tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите велосипед для удаления.")
            return

        bike_id = self.bikes_tree.item(selected_item[0])['values'][0]

        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот велосипед?"):
            db.delete_bike(self.conn, bike_id)
            messagebox.showinfo("Успех", "Велосипед успешно удален.")
            self.populate_bikes_table()
            self.clear_bike_inputs()

    def select_bike(self, event):
        """Заполняет поля ввода данными из выбранного велосипеда."""
        selected_item = self.bikes_tree.selection()
        if selected_item:
            bike = self.bikes_tree.item(selected_item[0])['values']
            self.bike_name_var.set(bike[1])
            self.bike_type_var.set(bike[2])
            self.bike_size_var.set(bike[3])
            self.rental_price_var.set(bike[4])
            self.availability_var.set(bike[5])

    def clear_bike_inputs(self):
        """Очищает поля ввода для велосипедов."""
        self.bike_name_var.set("")
        self.bike_type_var.set("")
        self.bike_size_var.set("")
        self.rental_price_var.set(0.0)
        self.availability_var.set(1)

    # TODO: Создать init_customers_tab, init_rentals_tab, init_summary_tab
    # и соответствующие функции для работы с клиентами, арендами и отчетами

    def __del__(self):
        if self.conn:
            self.conn.close()

if __name__ == '__main__':
    root = tk.Tk()
    app = RentalApp(root)
    root.mainloop()
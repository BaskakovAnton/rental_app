import tkinter as tk
from gui import RentalApp

def main():
    root = tk.Tk()
    app = RentalApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
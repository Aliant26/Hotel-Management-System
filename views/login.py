from customtkinter import *
from tkinter import messagebox

from views.window import Window
from models.users import check_login


class LoginApp(CTk):

    def __init__(self):
        super().__init__()

        self.title("Logowanie")
        self.geometry("300x300")

        CTkLabel(self, text="Login").pack(pady=10)

        self.username_entry = CTkEntry(self)
        self.username_entry.pack(pady=5)

        CTkLabel(self, text="Hasło").pack(pady=10)

        self.password_entry = CTkEntry(self, show="*")
        self.password_entry.pack(pady=5)

        self.log_button = CTkButton(
            self,
            text="Zaloguj",
            command=self.login
        )

        self.log_button.pack(pady=20)

        self.bind(
            "<Return>",
            lambda event: self.login()
        )

    def login(self):

        username = self.username_entry.get()
        password = self.password_entry.get()

        if check_login(username, password):

            self.destroy()

            app = Window()
            app.mainloop()

        else:
            messagebox.showerror(
                "Błąd",
                "Nieprawidłowy login lub hasło"
            )

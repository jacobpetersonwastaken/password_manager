from sign_in_box import SignInBox
from password_input import PasswordInput
from tkinter import *
HEIGHT = 200
WIDTH = 200



signin = SignInBox()


if signin.login_success:
        window = Tk()
        window.title("Password Manager")
        window.configure(padx=45, pady=45)
        password = PasswordInput()
        window.mainloop()

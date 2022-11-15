import pandas as pd
from tkinter import *
import tkinter.messagebox
import os
from cryptography.fernet import Fernet

USER_DATA = "data/login_user_and_pass.csv"
HEIGHT = 20
WIDTH = 300


def clickExitButton():
    exit()


class SignInBox:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title('Login')
        self.login_success = False

        canvas = Canvas(height=HEIGHT, width=WIDTH)
        canvas.grid(row=1, column=1)

        main_label = Label(text="Password Manager", font=('Helvetica', 18, 'bold'))
        main_label.grid(row=0, column=1)
        username_label = Label(text="Username:")
        username_label.grid(row=1, column=0)
        self.username_entry = Entry(width=40)
        self.username_entry.grid(row=1, column=1)
        self.username_entry.focus()
        password_label = Label(text="Password:")
        password_label.grid(row=2, column=0)
        self.password_entry = Entry(width=40)
        self.password_entry.grid(row=2, column=1)
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)
        self.pass_input = None
        self.encoded_pass = None
        self.decoded_pass = None

        login_button = Button(text="Login", width=40, command=self.authenticate)
        login_button.grid(row=3, column=1, padx=10, pady=10)
        if os.stat('data/info.csv').st_size == 0:
            self.new_user = True
        else:
            self.new_user = False


        mainloop()

    def check_new_user(self):
        if self.new_user:
            tkinter.messagebox.showwarning(title='"New User"', message="Set Username and password in the form below.")

    def authenticate(self):
        if self.new_user:
            if len(self.username_entry.get()) == 0 or len(self.password_entry.get()) == 0:
                tkinter.messagebox.showwarning(title='Info', message='Each field must be filled in.')
            else:
                self.new_user = False

                pass_input = self.password_entry.get()
                encoded_pass = self.fernet.encrypt(pass_input.encode())
                enc_pass_str = str(encoded_pass, 'utf-8')

                data = ['password manager app', self.username_entry.get(), enc_pass_str]
                data_labels = ['website', 'username', 'password']
                self.df = pd.DataFrame(data=[data], columns=list(data_labels))
                self.df.to_csv(USER_DATA, index=False)
                key_str = str(self.key, 'utf-8')
                login_data = ['user login', key_str, self.new_user]
                login_label = ['login', 'key', 'new user']
                df2 = pd.DataFrame(data=[login_data], columns=list(login_label))
                df2.to_csv('info.csv', index=False)

                tkinter.messagebox.showinfo(title='Success', message="New user login was successful")
                self.login_success = True

                self.window.destroy()
        elif not self.new_user:
            df2 = pd.read_csv('data/info.csv', index_col=False)
            right_key = (df2.iloc[df2.loc[df2['login'].str.contains('user login')].index[0], 1]).encode()

            f = Fernet(right_key)

            df = pd.read_csv(USER_DATA, index_col=False)
            saved_username = df.loc[df['website'].str.contains('password manager app')]
            saved_user_row = saved_username.index[0]
            find_saved_username = df.iloc[saved_user_row, 1]
            find_saved_password = df.iloc[saved_user_row, 2]

            byte_pw = find_saved_password.encode()
            decoded_pass = f.decrypt(byte_pw).decode()

            if self.username_entry.get() == find_saved_username and self.password_entry.get() == \
                    decoded_pass:
                tkinter.messagebox.showinfo(title='Success', message="Login was successful")
                self.login_success = True
                self.window.destroy()
            else:
                tkinter.messagebox.showwarning(title='Info', message='Wrong username or password.')


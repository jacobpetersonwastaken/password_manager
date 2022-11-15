import tkinter.messagebox
from tkinter import *
import pandas as pd
from random_password import RandomPassword
from cryptography.fernet import Fernet
import re

HEIGHT = 300
WIDTH = 200
rand_pass = RandomPassword()
USER_DATA = "data/login_user_and_pass.csv"


def clickExitButton():
    exit()


class PasswordInput:
    def __init__(self):
        self.result = 0
        self.df = pd.read_csv(USER_DATA, index_col=False)
        canvas = Canvas(height=HEIGHT, width=WIDTH)
        self.logo_img = PhotoImage(file="images/logo.png")
        canvas.create_image(100, 100, image=self.logo_img)
        canvas.grid(row=1, column=1)
        self.username_saved = False
        website_label = Label(text="Website:")
        website_label.grid(row=2, column=0)
        self.website_entry = Entry(width=34)
        self.website_entry.grid(row=2, column=1)
        self.website_entry.focus()
        self.search_button = Button(text="Search website", width=15, command=self.search_site)
        self.search_button.grid(row=2, column=2)
        username_label = Label(text="Email/Username:")
        username_label.grid(row=3, column=0)
        self.username_entry = Entry(width=53)
        self.username_entry.grid(row=3, column=1, columnspan=2)
        password_label = Label(text="Password:")
        password_label.grid(row=4, column=0)
        self.password_entry = Entry(width=34)
        self.password_entry.grid(row=4, column=1)
        add_button = Button(text="Add", width=45, command=self.add_func)
        add_button.grid(row=5, column=1, columnspan=2)
        gen_pass_button = Button(text="Generate Password", width=15, command=self.randomizer)
        gen_pass_button.grid(row=4, column=2)
        exit_button = Button(text="Exit", command=clickExitButton)
        exit_button.grid(row=0, column=3)
        self.username_check_box = IntVar()
        self.check_button = Checkbutton(text="Use saved username", variable=self.username_check_box,
                                        command=self.checkbutton_used)
        self.next_button = Button(text="next", width=15, command=self.next_result)
        self.result_label = Label(text='results')
        self.username_check_box.get()
        self.check_button.grid(row=3, column=3)
        self.change_user_box = IntVar()
        self.change_user_button = Checkbutton(text="Change saved username", variable=self.change_user_box,
                                              command=self.checkbutton_used)
        self.change_user_box.get()
        self.change_user_button.grid(row=4, column=3)
        self.check_saved_username()

        self.df2 = pd.read_csv('data/info.csv', index_col=False)
        self.right_key = (self.df2.iloc[self.df2.loc[self.df2['login'].str.contains('user login')].index[0], 1]).encode()



        self.fernet = Fernet(self.right_key)
        self.pass_input = None
        self.encoded_pass = None
        self.decoded_pass = None


    def check_saved_username(self):
        saved_username = self.df.loc[self.df['website'].str.contains('saved username')]
        if len(saved_username) == 0:
            self.change_user_button['state'] = DISABLED
            # print('nothing here')
            self.check_button['text'] = 'save username for future use'
        else:
            self.username_saved = True
            self.change_user_button['state'] = NORMAL
            self.check_button['text'] = 'Use saved username'

    def checkbutton_used(self):
        saved_username = self.df.loc[self.df['website'].str.contains('saved username')]
        if self.change_user_box.get() == 1:
            erase_old_user = tkinter.messagebox.askyesno(title='Confirmation', message='This will erase your current '
                                                                                       'saved username')
            if erase_old_user:
                saved_user_row = int(saved_username.index[0])
                self.df.drop(saved_user_row, inplace=True)
                self.username_saved = False
                self.check_button['state'] = DISABLED
                self.username_entry.delete(0, "end")
            else:
                self.change_user_box.set(0)
        elif self.username_saved:
            saved_user_row = int(saved_username.index[0])
            find_saved_username = self.df.iloc[saved_user_row, 1]
            if self.username_check_box.get() == 1:
                self.username_entry.delete(0, "end")
                self.username_entry.insert(0, find_saved_username)
            if self.change_user_box.get() == 0:
                self.check_button['state'] = NORMAL
                x = self.change_user_box.get() == 0

    def add_func(self):
        self.next_button.grid_forget()
        self.search_button['text'] = 'Search'
        if len(self.website_entry.get()) == 0 or len(self.username_entry.get()) == 0 or \
                len(self.password_entry.get()) == 0:
            tkinter.messagebox.showwarning(title='info', message="fill in website box as well.")
        else:
            self.pass_input = self.password_entry.get()
            self.encoded_pass = self.fernet.encrypt(self.pass_input.encode())
            str_pw = str(self.encoded_pass, 'utf-8')

            if not self.username_saved:
                if self.username_check_box.get() == 1 or self.change_user_box.get() == 1:
                    df2 = pd.DataFrame([['saved username', self.username_entry.get(), 'doesntmatter'],
                                        [self.website_entry.get(), self.username_entry.get(),
                                         str_pw]], columns=list(['website', 'username', 'password']))
                    self.df = self.df.append(df2, ignore_index=True)
                    self.df.to_csv(USER_DATA, index=False)
                    self.username_saved = True
                    self.reset_entry()
                    tkinter.messagebox.showinfo(title='Success', message="Your information was added and saved.")
                else:
                    self.df.loc[len(self.df.index)] = [self.website_entry.get(), self.username_entry.get(),
                                                       str_pw]
                    # print(self.df)
                    # x = input("waiting for userinput to save")
                    self.df.to_csv(USER_DATA, index=False)
                    self.reset_entry()
                    tkinter.messagebox.showinfo(title='Success', message="Your information was added and saved.")
            else:
                self.df.loc[len(self.df.index)] = [self.website_entry.get(), self.username_entry.get(),
                                                   str_pw]
                self.df.to_csv(USER_DATA, index=False)
                self.reset_entry()
                tkinter.messagebox.showinfo(title='Success', message="Your information was added and saved.")

    def reset_entry(self):
        self.username_check_box.set(0)
        self.change_user_box.set(0)
        self.website_entry.delete(0, "end")
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.check_saved_username()

    def search_site(self):
        self.result = 0
        if len(self.website_entry.get()) == 0:
            tkinter.messagebox.showwarning(title='Info', message='Website field must be filled in.')
        else:
            self.next_button.grid_remove()
            search_word = self.website_entry.get()
            searching = self.df.loc[self.df['website'].str.contains(f'^{search_word}[a-z]*', flags=re.I, regex=True)]
            search_results = [rows for rows in searching.index]
            self.search_button['text'] = f'Showing {len(search_results)} results'

            if len(searching) == 0:
                tkinter.messagebox.showwarning(title='Info', message='No website found')
            elif len(searching) > 1:
                self.next_button.grid(row=2, column=3)
                search_row = searching.index[0]

                find_saved_site = self.df.iloc[search_row, 0]
                find_saved_username = self.df.iloc[search_row, 1]
                find_saved_password = self.df.iloc[search_row, 2]

                byte_pw = find_saved_password.encode()
                self.decoded_pass = self.fernet.decrypt(byte_pw).decode()


                # byte_pw = find_saved_password.encode()
                # self.decoded_pass = self.fernet.decrypt(byte_pw).decode()

                self.update_user_pass(find_saved_site, find_saved_username, self.decoded_pass)
            else:
                search_row = searching.index[0]
                find_saved_site = self.df.iloc[search_row, 0]
                find_saved_username = self.df.iloc[search_row, 1]
                find_saved_password = self.df.iloc[search_row, 2]


                byte_pw = find_saved_password.encode()
                self.decoded_pass = self.fernet.decrypt(byte_pw).decode()

                self.update_user_pass(find_saved_site, find_saved_username, self.decoded_pass)

    def next_result(self):
        search_word = self.website_entry.get()
        searching = self.df.loc[self.df['website'].str.contains(f'^{search_word}[a-z]*', flags=re.I, regex=True)]
        search_results = [rows for rows in searching.index]
        if self.next_button['text'] == 'Back':
            self.search_button['text'] = f'Result {self.result} of {len(search_results)}'
            self.result -= 1
            currently_viewing = search_results[self.result]
            find_saved_site = self.df.iloc[currently_viewing, 0]
            find_saved_username = self.df.iloc[currently_viewing, 1]
            find_saved_password = self.df.iloc[currently_viewing, 2]
            byte_pw = find_saved_password.encode()
            self.decoded_pass = self.fernet.decrypt(byte_pw).decode()

            self.update_user_pass(find_saved_site, find_saved_username, self.decoded_pass)
            if search_results[self.result] == search_results[0]:
                self.next_button['text'] = 'Next'
        else:
            self.result += 1
            self.search_button['text'] = f'Result {self.result + 1} of {len(search_results)}'
            currently_viewing = search_results[self.result]
            find_saved_site = self.df.iloc[currently_viewing, 0]
            find_saved_username = self.df.iloc[currently_viewing, 1]
            find_saved_password = self.df.iloc[currently_viewing, 2]
            byte_pw = find_saved_password.encode()
            self.decoded_pass = self.fernet.decrypt(byte_pw).decode()

            self.update_user_pass(find_saved_site, find_saved_username, self.decoded_pass)
            if search_results[self.result] == search_results[-1]:
                self.next_button['text'] = 'Back'





    def update_user_pass(self, find_saved_site, find_saved_username, decoded_pass):
        self.website_entry.delete(0, "end")
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.website_entry.insert(0, find_saved_site)
        self.username_entry.insert(0, find_saved_username)
        self.password_entry.insert(0, decoded_pass)



    def randomizer(self):
        rand_pass_ = rand_pass.randomizer()
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, rand_pass_)

import sys, os, socket
import general_functions as g_func
import client.client_functions as c_func
from tkinter import *
from tkinter import filedialog
import pygame

pygame.init()

"""Constants"""
FONT = ('calibre', 18, 'bold')
ADDRESS = ('192.168.29.137', 3000)
TEST_VID = r'C:\Users\derio_ipprk9s\PycharmProjects\MediaStreamer\V-Dah1L9oIg.mp4'
BUFFSIZE = 2048
SIZE = '800x400+200+50'
MAIN_FLAG = False
STORAGE = ''


def startup(order):
    click()

    result_label.forget()
    name = user_entry.get()
    passw = passw_entry.get()
    print(name, passw)
    user_entry.delete(0, END)
    passw_entry.delete(0, END)
    res = 'Username and password must be over 3 ch'
    try:
        if len(name) > 3 and len(passw) > 3:
            if order == 1:
                res = c_func.login(client, name, passw, root)
            elif order == 2:
                res = c_func.signup(client, name, passw, root)
        if res != 'success':
            result_var.set(res)
            result_label.grid(columnspan=2, row=4, column=0)
        else:
            result_var.set(name)
            global MAIN_FLAG
            MAIN_FLAG = True
    except socket.error as socketerror:
        print('Error:', socketerror)
        root.destroy()
        create_error(socketerror)


def download_act():
    click()

    filename = listbox.get(listbox.curselection())
    if filename in os.listdir(STORAGE):
        return
    print(filename)
    try:
        c_func.download(client, filename, STORAGE)
    except socket.error as socketerror:
        print('Error:', socketerror)
        root.destroy()
        create_error(socketerror)


def click():
    pygame.mixer.music.load('Menu-Selection-Change.mp3')  # Loading File Into Mixer
    pygame.mixer.music.play()


def play():
    click()
    filename = listbox.get(listbox.curselection())
    print(filename)
    try:
        c_func.play_a_file(client, filename, STORAGE)
    except socket.error as socketerror:
        print('Error:', socketerror)
        root.destroy()
        create_error(socketerror)


def browsefunc():
    click()
    ent1.delete(0, END)
    path.set(filedialog.askopenfilename(filetypes=(("Mp3 files", "*.mp3"), ("All files", "*.*"))).replace('/', '\\'))
    filename = path.get().split('\\')[-1]
    ent1.insert(END, filename)  # add this


def create_error(error):
    click()

    new = Tk()
    Label(new, text=error, font=FONT).grid()
    new.mainloop()
    client.send('done'.encode())
    client.close()
    sys.exit()


def upload():
    click()

    fpath = path.get()
    name = fpath.split('\\')[-1]
    if name in files:
        return
    try:
        g_func.upload_vid(client, fpath)
    except socket.error as socketerror:
        print('Error:', socketerror)
        root.destroy()
        create_error(socketerror)
    files.append(name)
    listbox.insert(END, name)


if __name__ == '__main__':
    # Try to connect.
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(ADDRESS)
    except socket.error as socketerror:
        print('Error:', socketerror)
        create_error(socketerror)
    # Startup signing in.
    root = Tk()
    result_var = StringVar()
    result_label = Label(root, textvariable=result_var, font=FONT, wraplength=300, justify=LEFT)
    SUCCESS = False
    try:
        # Startup signing in.
        Label(root, text='Username:', font=FONT).grid(row=0, column=0)
        user_entry = Entry(root, font=FONT)
        Label(root, text='Password:', font=FONT).grid(row=1, column=0)
        passw_entry = Entry(root, font=FONT)
        Button(root, text='LOGIN', font=FONT, command=lambda: startup(1)).grid(row=2, column=0)
        Button(root, text='REGISTER', font=FONT, command=lambda: startup(2)).grid(row=2, column=1)
        user_entry.grid(row=0, column=1)
        passw_entry.grid(row=1, column=1)
        root.mainloop()
        if not MAIN_FLAG:
            client.send('done'.encode())
            client.close()
            sys.exit()
        # Welcome msg.
        app = Tk()
        Label(app, text='$ WELCOME TO CLOUD MASTER $', font=('calibre', 50, 'bold'), fg='green').pack()
        app.after(4600, lambda: app.destroy())
        app.mainloop()
        # Main window.
        STORAGE = 'downloads\\' + result_var.get()
        if not os.path.isdir(STORAGE):
            os.mkdir(STORAGE)
        root = Tk()
        path = StringVar('')
        Label(root, text='{0}\'s Storage'.format(result_var.get().capitalize()), font=FONT, bg="grey").grid(row=0,
                                                                                                            column=0)
        Label(root, text='Files', font=FONT, bg="grey").grid(row=1, column=0)
        listbox = Listbox(root, height=5, width=25, bg="grey", activestyle='dotbox', font="Helvetica", fg="yellow")
        listbox.grid(row=1, column=1)
        scrollbar = Scrollbar(root)
        scrollbar.grid(row=1, column=2)
        files = c_func.get_files(client)
        for values in files:
            listbox.insert(END, values)
        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        Button(root, text='Download', font=FONT, command=download_act, bg="green").grid(row=1, column=3)
        Button(root, text='Play', font=FONT, command=play, bg="green").grid(row=1, column=4)
        ent1 = Entry(root, font=FONT, bg="grey")
        Label(root, text='Path: ', font=FONT, bg="grey").grid(row=3, column=0)
        ent1.grid(row=3, column=1)
        Button(root, text="Browse", font=40, command=browsefunc, bg="green").grid(row=3, column=2)
        Button(root, text="Upload", font=40, command=upload, bg="green").grid(row=3, column=3)
        root.mainloop()
    except socket.error as socketerror:
        print('Error:', socketerror)
        root.destroy()
        create_error(socketerror)
    client.send('done'.encode())
    client.close()

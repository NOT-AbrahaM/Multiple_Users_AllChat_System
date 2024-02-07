import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '127.0.0.1'
PORT = 9999
DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
BLUE = '#1DA1F2'
PINK = '#D62976'
ORANGE = '#FA7E1E'
WHITE = "white"
BLACK = "black"
FONT = ("Georgia", 17)
BUTTON_FONT = ("Georgia", 14)
SMALL_FONT = ("Georgia", 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def add_a_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)


def connect():
    try:
        client.connect((HOST, PORT))
        print("[SUCCESS] Successfully Connected to The Server")
        add_a_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")
        username = username_textbox.get()
        if username != '':
            client.sendall(username.encode())
        else:
            messagebox.showerror("Invalid Username", "Usernames cannot be empty")
        threading.Thread(target=listen_message_server, args=(client,)).start()
        username_textbox.config(state=tk.DISABLED)
        username_button.config(state=tk.DISABLED)


def send_a_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Its a Empty message", "Messages cannot be empty")


root = tk.Tk()
root.geometry("600x600")
root.title("ONLINE Chat System ")
root.resizable(False, False)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="ENTER USERNAME:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=8)

username_textbox = tk.Entry(top_frame, font=FONT, bg=WHITE, fg=BLACK, width=20)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="JOIN", font=BUTTON_FONT, bg=BLUE, fg=BLACK, command=connect)
username_button.pack(side=tk.LEFT, padx=8)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=WHITE, fg=BLACK, width=35)
message_textbox.pack(side=tk.LEFT, padx=12)

message_button = tk.Button(bottom_frame, text="SEND", font=BUTTON_FONT, bg=BLUE, fg=BLACK, command=send_a_message)
message_button.pack(side=tk.LEFT, padx=5)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=DARK_GREY, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_message_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]
            add_a_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")


def main():
    root.mainloop()


if __name__ == '__main__':
    main()

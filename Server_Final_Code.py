import socket
import threading

HOST = '127.0.0.1'
PORT = 9999
LISTENER_LIMIT = 5
active_clients = []


def listen_to_message(client, username):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            send_messages_to_everyone(final_msg)
        else:
            print(f"The message sent from client {username} is empty")


def send_message_to_client(client, message):
    client.sendall(message.encode())


def send_messages_to_everyone(message):
    for user in active_clients:
        send_message_to_client(user[1], message)


def client_side(client):
    username = client.recv(2048).decode('utf-8')
    if username != '':
        active_clients.append((username, client))
        prompt_message = "SERVER~" + f"{username} Has Hopped into the Chat"
        prompt_messages = "SERVER~" + f"Don't Forget To Say Hi to {username}"
        send_messages_to_everyone(prompt_message)
        send_messages_to_everyone(prompt_messages)
        threading.Thread(target=listen_to_message, args=(client, username,)).start()
    else:
        print("Client username is empty")

    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} Has Hopped into the Chat"
            prompt_messages = "SERVER~" + f"Don't Forget To Say Hi to {username}"
            send_messages_to_everyone(prompt_message)
            send_messages_to_everyone(prompt_messages)
            threading.Thread(target=listen_to_message, args=(client, username,)).start()
        else:
            print("You are the Only One Here")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    server.listen(LISTENER_LIMIT)

    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}.....")
        threading.Thread(target=client_side, args=(client,)).start()


if __name__ == '__main__':
    main()

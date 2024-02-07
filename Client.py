import socket

Client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Client.connect(("localhost", 9999))

done=False

while not done:
    Client.send(input ("Message From Client to The Server : ").encode('utf-8')) 
    msg = Client.recv(1024).decode('utf-8')
    if msg == "exit":
        done = True
    else:
        print("Reply From The Server : ", msg)

Client.close()

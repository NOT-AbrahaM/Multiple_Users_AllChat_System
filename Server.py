import socket
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
Server.bind(("localhost", 9999))

Server.listen()
print("[WAITING] Waiting For a Client to Connect .........")
print("\n")
Client, addr = Server.accept()
print("[SUCCESS] Server Connected With ", addr)
print("\n")   
done=False

while not done:
    msg = Client.recv(1024).decode('utf-8')

    if msg == "exit":
        done = True
    else:
        print("Message From the Client : ",msg)

    Client.send(input("Message From Server to the Client : ").encode("utf-8"))
Client.close()
Server.close()


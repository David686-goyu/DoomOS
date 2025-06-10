# server.py
import socket
import threading

clients = {}
HOST = '127.0.0.1'
PORT = 12345

def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                del clients[client]

def handle_client(client_socket):
    name = f"User{len(clients)+1}"
    clients[client_socket] = name
    client_socket.send("Welcome! Type /help for commands.\n".encode())

    while True:
        try:
            msg = client_socket.recv(1024).decode().strip()
            if msg.startswith("/"):
                if msg.startswith("/name "):
                    new_name = msg[6:].strip()
                    broadcast(f"{clients[client_socket]} is now {new_name}")
                    clients[client_socket] = new_name
                elif msg == "/help":
                    client_socket.send(b"Commands:\n  /name <newname>\n  /help\n  /exit\n")
                elif msg == "/exit":
                    broadcast(f"{clients[client_socket]} has left the chat.")
                    client_socket.close()
                    del clients[client_socket]
                    break
                else:
                    client_socket.send(b"Unknown command. Type /help\n")
            else:
                broadcast(f"{clients[client_socket]}: {msg}", client_socket)
        except:
            client_socket.close()
            del clients[client_socket]
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()

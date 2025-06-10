import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print(message)
        except:
            print("Disconnected from server.")
            break

def send_messages(sock):
    while True:
        msg = input()
        sock.send(msg.encode())
        if msg.strip() == "/exit":
            sock.close()
            sys.exit()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()
    send_messages(client)

if __name__ == "__main__":
    main()

import socket
import threading

clients = {}

def broadcast(message, _client_socket):
    for client_socket in clients:
        if client_socket != _client_socket:
            try:
                client_socket.send(message)
            except:
                client_socket.close()
                del clients[client_socket]

def handle_client(client_socket):
    username = clients[client_socket]
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            formatted_message = f"{username}: {message.decode('utf-8')}".encode('utf-8')
            broadcast(formatted_message, client_socket)
        except:
            break

    client_socket.close()
    del clients[client_socket]

def main():
    host = '127.0.0.1'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f'[*] Listening on {host}:{port}')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == '__main__':
    main()
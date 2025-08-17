# -*- coding: utf-8 -*-

import socket
import threading

# 클라이언트 소켓을 키로, 사용자 이름을 값으로 저장하는 딕셔너리
clients = {}

# 메시지 브로드캐스팅 함수
def broadcast(message, _client_socket):
    # 모든 클라이언트에게 메시지 전송
    for client_socket in clients:
        # 메시지를 보낸 클라이언트는 제외
        if client_socket != _client_socket:
            try:
                client_socket.send(message)
            except:
                # 오류 발생 시 클라이언트 소켓을 닫고 딕셔너리에서 제거
                client_socket.close()
                del clients[client_socket]

# 클라이언트 처리 함수
def handle_client(client_socket):
    # 현재 클라이언트의 사용자 이름 가져오기
    username = clients[client_socket]
    while True:
        try:
            # 클라이언트로부터 메시지 수신
            message = client_socket.recv(1024)
            if not message:
                break
            # 사용자 이름과 함께 메시지 포맷팅
            formatted_message = f"{username}: {message.decode('utf-8')}".encode('utf-8')
            # 다른 클라이언트에게 메시지 브로드캐스팅
            broadcast(formatted_message, client_socket)
        except:
            break

    # 클라이언트 연결 종료 시 소켓을 닫고 딕셔너리에서 제거
    client_socket.close()
    del clients[client_socket]

# 메인 함수
def main():
    host = '127.0.0.1'  # 호스트 주소
    port = 8080  # 포트 번호

    # 서버 소켓 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 소켓을 주소와 포트에 바인딩
    server_socket.bind((host, port))
    # 연결 대기
    server_socket.listen(5)

    print(f'[*] Listening on {host}:{port}')

    while True:
        # 클라이언트 연결 수락
        client_socket, addr = server_socket.accept()
        print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')
        # 클라이언트로부터 사용자 이름 수신
        username = client_socket.recv(1024).decode('utf-8')
        # 클라이언트 딕셔너리에 추가
        clients[client_socket] = username
        # 각 클라이언트를 처리할 스레드 생성 및 시작
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == '__main__':
    main()

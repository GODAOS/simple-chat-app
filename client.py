# -*- coding: utf-8 -*-

import socket
import threading

# 서버로부터 메시지를 수신하는 함수
def receive_messages(client_socket):
    while True:
        try:
            # 서버로부터 메시지 수신 및 디코딩
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            # 수신된 메시지 출력
            print(message)
        except:
            break

# 메인 함수
def main():
    host = '127.0.0.1'  # 서버 호스트 주소
    port = 8080  # 서버 포트 번호

    # 클라이언트 소켓 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 서버에 연결
    client_socket.connect((host, port))

    # 사용자 이름 입력
    username = input("Enter your username: ")
    # 서버에 사용자 이름 전송
    client_socket.send(username.encode('utf-8'))

    # 메시지 수신을 위한 스레드 생성 및 시작
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        # 사용자로부터 메시지 입력
        message = input()
        # 'exit' 입력 시 루프 종료
        if message.lower() == 'exit':
            break
        # 서버에 메시지 전송
        client_socket.send(message.encode('utf-8'))

    # 클라이언트 소켓 닫기
    client_socket.close()

if __name__ == '__main__':
    main()

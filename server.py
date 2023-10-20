import cv2
import socket
import threading
from ui import VideoChatUI
import tkinter as tk

class VideoChatServer:
    def __init__(self):
        self.ui = VideoChatUI(tk.Tk(), "화상 채팅 서버")
        self.ui.on_send_message = self.send_message_to_clients
        self.clients = []

        # 웹캠 초기화
        self.cap = cv2.VideoCapture(0)

        # 소켓 초기화
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 50001))
        self.server_socket.listen(5)

        # 웹캠 영상 전송 스레드 시작
        self.webcam_thread = threading.Thread(target=self.send_webcam)
        self.webcam_thread.daemon = True
        self.webcam_thread.start()

        # 클라이언트 연결을 처리하는 스레드 시작
        self.receive_thread = threading.Thread(target=self.receive_clients)
        self.receive_thread.deamon = True
        self.receive_thread.start()

        # 서버 GUI 시작
        tk.mainloop()

    def show_frame(self, frame):
        self.ui.show_frame(frame)

    def send_message_to_clients(self, message):
        for client in self.clients:
            client.send(message.encode())

        # 서버 UI에도 메시지 표시
        self.ui.receive_message("서버: " + message)

    def send_message_to_server(self, message):
        self.ui.receive_message(message)
        self.send_message_to_clients(message)

    def send_webcam(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue
            _, encoded_frame = cv2.imencode('.jpg',frame,
    [int(cv2.IMWRITE_JPEG_QUALITY), 60])
            encoded_frame = encoded_frame.tobytes()
            for client in self.clients:
                try:
                    client.send(encoded_frame)
                except:
                    self.clients.remove(client)
                self.show_frame(frame)
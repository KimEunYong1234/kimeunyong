import socket
import cv2

class VideoChatClient:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.client_socket = None
        self.video_capture = cv2.VideoCapture(0)

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_address, self.server_port))
            print("연결 성공")
        except Exception as e:
            print("연결 오류:", str(e))

    def send_message_to_server(self, message):
        self.client_socket.send(message.encode())

    def receive_message(self):
        return self.client_socket.recv(1024).decode()

    def display_video_stream(self):
        ret, frame = self.video_capture.read()
        return frame

    def send_video_stream(self, frame):
        _, encoded_frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        encoded_frame = encoded_frame.tobytes()
        self.client_socket.send(encoded_frame)

    def close(self):
        self.client_socket.close()

if __name__ == "__main__":
    server_address = 'localhost'  # 서버의 실제 IP 주소로 변경
    server_port = 50001

    client = VideoChatClient(server_address, server_port)
    client.connect_to_server()

    try:
        while True:
            frame = client.display_video_stream()
            client.send_video_stream(frame)

            message = client.receive_message()
            if message:
                print("서버 메시지:", message)

    except KeyboardInterrupt:
        client.close()

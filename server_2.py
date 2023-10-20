import socket
import cv2
import pickle
import struct
import threading

# 서버 IP 주소 및 포트 설정
server_ip = 'localhost'
server_port = 50001

# 소켓 객체 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(5)
print(f"서버 대기 중... ({server_ip}:{server_port})")

# 클라이언트로부터 비디오 프레임을 받아들이고 다시 브로드캐스트하는 함수
def client_handler(client_socket, client_address):
    print(f"클라이언트 연결: {client_address}")

    # OpenCV를 사용하여 웹캠 초기화
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    try:
        while True:
            # 프레임 읽기
            retval, frame = capture.read()

            # 이미지 인코딩
            retval, frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            data = pickle.dumps(frame)

            # 데이터 길이 전송
            client_socket.sendall(struct.pack(">Q", len(data)))

            # 데이터 전송
            client_socket.sendall(data)
    except Exception as e:
        print(f"클라이언트 {client_address} 연결 종료: {str(e)}")
        client_socket.close()
        capture.release()

# 클라이언트 연결 대기 및 스레드 생성
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=client_handler, args=(client_socket, client_address))
    client_thread.start()

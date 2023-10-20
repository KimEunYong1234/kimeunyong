import socket
import cv2
import pickle
import struct
import threading

# 서버 IP 주소 및 포트 설정
server_ip = 'localhost'
server_port = 50001

# 소켓 객체 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))
print("서버에 연결되었습니다.")

# 비디오 스트림 표시 함수
def display_video_stream(client_socket):
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
        print(f"연결 종료: {str(e)}")
        client_socket.close()
        capture.release()

# 비디오 스트림 수신 및 표시 스레드 시작
video_thread = threading.Thread(target=display_video_stream, args=(client_socket,))
video_thread.start()



# 비디오 스트림 수신 대기
try:
    while True:
        pass
except KeyboardInterrupt:
    print("클라이언트 종료")
    client_socket.close()

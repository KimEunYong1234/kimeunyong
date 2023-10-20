from tkinter import Tk, Label, Entry, Button, Text, END
from PIL import Image, ImageTk
import cv2
import threading

class VideoChatUI:
    def __init__(self, window, title):
        self.window = window
        self.window.title(title)

        # 웹캠 이미지 라벨
        self.label = Label(window)
        self.label.grid(row=0, column=0, padx=10, pady=10, rowspan=2, sticky="nsew")

        # 채팅 창 (Text 위젯)
        self.chat_text = Text(window, wrap="none")
        self.chat_text.grid(row=0, column=1, padx=10, pady=10, rowspan=2, sticky="nsew")

        # 메시지 입력 필드
        self.entry = Entry(window)
        self.entry.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # 메시지 보내기 버튼
        self.send_button = Button(window, text="보내기", command=self.send_message)
        self.send_button.grid(row=2, column=1, padx=10, pady=10, sticky="se")

        # 행 및 열 가중치 설정
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.grid_rowconfigure(2, weight=1)
        window.grid_columnconfigure(0, weight=4)  # 비디오 화면이 80% 차지
        window.grid_columnconfigure(1, weight=1)  # 채팅 창이 20% 차지

    def show_frame(self, frame):
        # OpenCV에서 읽은 프레임을 Tkinter 이미지로 변환
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.label.config(image=photo)
        self.label.image = photo

    def send_message(self):
        message = self.entry.get()
        if message:
            self.entry.delete(0, END)
            self.on_send_message(message)

    def on_send_message(self, message):
        pass

    def receive_message(self, message):
        self.chat_text.config(state="normal")
        self.chat_text.insert(END, message + '\n')
        self.chat_text.config(state="disabled")

# 웹캠 이미지를 업데이트하는 스레드
def update_video_stream(ui):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            ui.show_frame(frame)

if __name__ == "__main__":
    root = Tk()
    app = VideoChatUI(root, "Video Chat")

    # 웹캠 이미지를 업데이트하는 스레드 시작
    video_thread = threading.Thread(target=update_video_stream, args=(app,))
    video_thread.daemon = True
    video_thread.start()

    root.mainloop()

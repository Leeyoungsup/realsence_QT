import sys
import cv2
import numpy as np
import pyrealsense2 as rs
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer


class RealSenseViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # RealSense 초기화
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.pipeline.start(config)

        # PyQt 설정
        self.setWindowTitle("RealSense Viewer")
        self.setGeometry(100, 100, 640, 480)
        
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 타이머 설정
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            return

        # Numpy 배열로 변환
        color_image = np.asanyarray(color_frame.get_data())

        # OpenCV 이미지를 QImage로 변환
        h, w, ch = color_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(color_image.data, w, h, bytes_per_line, QImage.Format_BGR888)

        # QLabel에 표시
        self.label.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        # 프로그램 종료 시 RealSense 해제
        self.pipeline.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = RealSenseViewer()
    viewer.show()
    sys.exit(app.exec_())

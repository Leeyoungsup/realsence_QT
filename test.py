import sys
import cv2
import numpy as np
import pyrealsense2 as rs
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.uic import loadUi


class RealSenseViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load .ui file
        loadUi("front.ui", self)

        # Initialize RealSense
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.pipeline.start(config)

        # Initialize QGraphicsView and QGraphicsScene
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        # Set up timer for frame updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        # Get RealSense frame
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            return

        # Convert frame to numpy array
        color_image = np.asanyarray(color_frame.get_data())

        # Convert numpy array to QImage
        h, w, ch = color_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(color_image.data, w, h, bytes_per_line, QImage.Format_BGR888)

        # Convert QImage to QPixmap and display in QGraphicsView
        pixmap = QPixmap.fromImage(qt_image)
        self.scene.clear()  # Clear previous frame
        self.scene.addPixmap(pixmap)
        self.graphicsView.setScene(self.scene)

    def closeEvent(self, event):
        # Stop RealSense pipeline on close
        self.pipeline.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = RealSenseViewer()
    viewer.show()
    sys.exit(app.exec_())

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGraphicsTextItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class CameraView(QWidget):
    """각 카메라에 대해 RGB와 Depth 뷰 및 정보를 관리"""
    def __init__(self, parent_layout, camera_name, show_depth=True):
        super().__init__()

        self.camera_name = camera_name  # 카메라 이름 저장
        self.show_depth = show_depth  # Depth 뷰 표시 여부

        # 레이아웃 설정
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # 카메라 정보 표시 레이블
        self.camera_info_label = QLabel(f"Camera: {camera_name} | FPS: 0")
        self.camera_info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.camera_info_label)

        # RGB 뷰 추가
        self.rgb_view = QGraphicsView()
        self.rgb_scene = QGraphicsScene()
        self.rgb_view.setScene(self.rgb_scene)
        self.rgb_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.rgb_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.layout.addWidget(QLabel("RGB View", alignment=Qt.AlignCenter))
        self.layout.addWidget(self.rgb_view)

        # Depth 뷰 추가
        self.depth_view = QGraphicsView()
        self.depth_scene = QGraphicsScene()
        self.depth_view.setScene(self.depth_scene)
        self.depth_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.depth_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout.addWidget(QLabel("Depth View", alignment=Qt.AlignCenter))
        self.layout.addWidget(self.depth_view)

        # USB 2.0 메시지 표시 (초기값)
        if not self.show_depth:
            text_item = QGraphicsTextItem("USB 2.0입니다.")
            font = QFont()
            font.setPointSize(12)
            text_item.setFont(font)
            text_item.setDefaultTextColor(Qt.red)
            self.depth_scene.addItem(text_item)

            # 텍스트를 Depth 뷰의 중앙에 위치시키기
            scene_rect = self.depth_scene.sceneRect()
            text_item.setPos(
                scene_rect.width() / 2 - text_item.boundingRect().width() / 2,
                scene_rect.height() / 2 - text_item.boundingRect().height() / 2
            )

        # FPS 업데이트 타이머
        self.frame_count = 0
        self.fps = 0
        self.fps_timer = QTimer()
        self.fps_timer.timeout.connect(self.update_fps)
        self.fps_timer.start(1000)  # 1초마다 FPS 업데이트

        # 부모 레이아웃에 추가
        parent_layout.addWidget(self)

    def update_views(self, rgb_image, depth_colormap=None):
        """RGB 및 Depth 이미지를 업데이트"""
        # RGB 이미지 표시
        self.rgb_scene.clear()
        rgb_pixmap = self.convert_to_pixmap(rgb_image)
        self.rgb_scene.addPixmap(rgb_pixmap)
        self.rgb_view.fitInView(self.rgb_scene.itemsBoundingRect(), Qt.KeepAspectRatio)

        # Depth 이미지 표시
        self.depth_scene.clear()
        if self.show_depth and depth_colormap is not None:
            depth_pixmap = self.convert_to_pixmap(depth_colormap)
            self.depth_scene.addPixmap(depth_pixmap)
            self.depth_view.fitInView(self.depth_scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        else:
            text_item = QGraphicsTextItem("USB 2.0입니다.")
            font = QFont()
            font.setPointSize(12)
            text_item.setFont(font)
            text_item.setDefaultTextColor(Qt.red)
            self.depth_scene.addItem(text_item)

            # 텍스트를 Depth 뷰의 중앙에 위치시키기
            scene_rect = self.depth_scene.sceneRect()
            text_item.setPos(
                scene_rect.width() / 2 - text_item.boundingRect().width() / 2,
                scene_rect.height() / 2 - text_item.boundingRect().height() / 2
            )

        # 프레임 카운터 증가
        self.frame_count += 1
    def update_fps(self):
        """초당 프레임 수 업데이트"""
        self.fps = self.frame_count
        self.frame_count = 0
        self.camera_info_label.setText(f"Camera: {self.camera_name} | FPS: {self.fps}")

    @staticmethod
    def convert_to_pixmap(image):
        """Numpy 이미지를 QPixmap으로 변환"""
        h, w, ch = image.shape
        bytes_per_line = ch * w
        qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format_BGR888)
        return QPixmap.fromImage(qt_image)

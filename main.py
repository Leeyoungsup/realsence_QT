import sys
import pyrealsense2 as rs
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QListWidgetItem
from PyQt5.uic import loadUi
from display import CameraView
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import Qt, QTimer  # Qt 네임스페이스 추가
import numpy as np
import cv2
import copy


class RealSenseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI 로드
        loadUi("front.ui", self)

        # RealSense Context 초기화
        self.context = rs.context()
        self.devices = []  # 연결된 카메라 목록
        self.views = {}  # 카메라별 View와 Pipeline 관리
        self.timers = {}  # 각 카메라별 QTimer 관리
        self.streaming = False
        # UI 연결
        self.wholeCheck.stateChanged.connect(self.toggle_all_cameras)
        self.playButton.clicked.connect(self.start_streaming)
        self.cameraList.itemChanged.connect(self.toggle_camera_view)
        self.cameraList.itemDoubleClicked.connect(self.enable_item_edit) 
        # 카메라 목록 업데이트
        self.populate_camera_list()
    def enable_item_edit(self, item):
        """항목 더블클릭 시 편집 모드 활성화"""
        item.setFlags(item.flags() | Qt.ItemIsEditable) 
        
    def toggle_all_cameras(self, item):
        """모든 카메라의 상태를 일괄 변경"""
        for i in range(self.cameraList.count()):
            item = self.cameraList.item(i)
            item.setCheckState(2 if self.wholeCheck.checkState() else 0)
    def handle_item_change(self, item):
        """항목 이름 변경 시 처리"""
        print(f"Camera name updated to: {item.text()}")
        
        
    def populate_camera_list(self):
        """연결된 카메라 목록 표시"""
        self.cameraList.clear()
        self.devices = []

        for i, device in enumerate(self.context.query_devices()):
            name = device.get_info(rs.camera_info.name)
            self.devices.append(device)
            item = QListWidgetItem(f"{name} (ID: {i})")
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
            item.setCheckState(0)  # 체크박스 기본값: 체크되지 않음
            self.cameraList.addItem(item)
            
    def toggle_camera_view(self, item):
        """체크 상태에 따라 QGraphicsView 생성/제거"""
        camera_index = self.cameraList.row(item)
        device = self.devices[camera_index]

        if item.checkState():  # 체크됨
            self.add_camera_view(device, item)
        else:  # 체크 해제됨
            self.remove_camera_view(device)

    def add_camera_view(self, device, item):
        """QGraphicsView 추가 및 RealSense 파이프라인 설정"""
        if device in self.views:
            return  # 이미 존재하는 경우 무시

        # 카메라 정보 가져오기
        serial = device.get_info(rs.camera_info.serial_number)
        usb_type = device.get_info(rs.camera_info.usb_type_descriptor)

        # USB 포트 유형 확인
        is_usb_3 = usb_type.startswith("3.")

        # QGridLayout 설정
        layout = self.viewContainer.layout()
        if layout is None:
            layout = QGridLayout(self.viewContainer)
            self.viewContainer.setLayout(layout)

        # CameraView 생성 (item 텍스트를 camera_name으로 사용)
        camera_name = item.text()
        camera_view = CameraView(layout, camera_name, show_depth=is_usb_3)

        # 빈 셀 위치 찾기
        row, col = self.find_empty_cell(layout)

        # CameraView 배치
        layout.addWidget(camera_view, row, col, 1, 2)

        # RealSense 파이프라인 설정
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_device(serial)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        if is_usb_3:
            config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        pipeline.start(config)

        # QTimer 설정
        timer = QTimer()

        # 카메라 데이터 관리
        self.views[device] = (camera_view, pipeline)
        self.timers[device] = timer



    def find_empty_cell(self, layout):
        """2x2 그리드에서 빈 셀의 좌표를 찾음"""
        rows, cols = 2, 2  # 2x2 그리드
        occupied = set()

        # 현재 레이아웃에서 사용 중인 셀 찾기
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item is not None:
                row, col, _, _ = layout.getItemPosition(i)
                occupied.add((row, col))

        # 첫 번째 빈 셀 찾기
        for row in range(rows):
            for col in range(0, cols * 2, 2):  # RGB와 Depth는 같은 셀로 묶임
                if (row, col) not in occupied:
                    return row, col

        raise ValueError("No empty cells available")  # 셀이 부족한 경우 예외 처리
    def remove_camera_view(self, device):
        """QGraphicsView 제거 및 RealSense 파이프라인 중지"""
        if device not in self.views:
            return

        camera_view, pipeline = self.views.pop(device)
        timer = self.timers.pop(device)
        if self.streaming:
            self.start_streaming()
        # QTimer 중지
        timer.stop()

        # RealSense 파이프라인 중지
        pipeline.stop()

        # QGridLayout에서 위젯 제거
        layout = self.viewContainer.layout()
        layout.removeWidget(camera_view.rgb_view)
        layout.removeWidget(camera_view.depth_view)
        layout.removeWidget(camera_view)
        camera_view.deleteLater() 
        # 위젯 삭제
        camera_view.rgb_view.deleteLater()
        camera_view.depth_view.deleteLater()

    def update_frames(self, device):
        """카메라 프레임을 가져와 뷰에 업데이트"""
        if device not in self.views:
            return

        camera_view, pipeline = self.views[device]

        # RealSense 프레임 가져오기
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame() if camera_view.show_depth else None

        if not color_frame:
            return

        # RGB 이미지 업데이트
        color_image = np.asanyarray(color_frame.get_data())

        # Depth 이미지 업데이트 (USB 3.0인 경우만)
        depth_colormap = None
        if depth_frame:
            depth_image = np.asanyarray(depth_frame.get_data())
            depth_colormap = cv2.applyColorMap(
                cv2.convertScaleAbs(depth_image, alpha=0.2), cv2.COLORMAP_JET
            )

        # QGraphicsView 업데이트
        camera_view.update_views(color_image, depth_colormap)


    def start_streaming(self):
        """재생 버튼 클릭 시 스트리밍 시작"""
        if not self.streaming:
            for device, (camera_view, pipeline) in self.views.items():
                self.timers[device].timeout.connect(lambda dev=device: self.update_frames(dev))
                self.timers[device].start(30)  # 약 30 FPS로 업데이트
            self.streaming = True
            self.playButton.setText("중단")  # 버튼 텍스트 변경
        else:
            for device, (camera_view, pipeline) in self.views.items():
                self.timers[device].stop()
                self.timers[device] = QTimer()
                camera_view.rgb_scene.clear()  # RGB 뷰 초기화
                if camera_view.show_depth:    # Depth 뷰가 존재하는 경우만 초기화
                    camera_view.depth_scene.clear()  # Depth 뷰 초기화
            self.streaming = False
            self.playButton.setText("재생")

            
    def closeEvent(self, event):
        """종료 시 모든 파이프라인 및 QTimer 정리"""
        for device, (camera_view, pipeline) in self.views.items():
            pipeline.stop()
        for timer in self.timers.values():
            timer.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = RealSenseApp()
    viewer.show()
    sys.exit(app.exec_())
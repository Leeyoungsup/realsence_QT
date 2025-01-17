import sys
import pyrealsense2 as rs
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QListWidgetItem
from PyQt5.uic import loadUi
from display import CameraView
from PyQt5.QtWidgets import QGridLayout,QTreeWidgetItem
from PyQt5.QtCore import Qt, QTimer  # Qt 네임스페이스 추가
import numpy as np
import cv2
import copy
import os
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog
import json
from PyQt5.QtWidgets import QProxyStyle, QStyle
from PyQt5.QtWidgets import QStyledItemDelegate
import naver_stt
import gpt_sample
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
def populate_tree(tree, json_data):
    def add_items(parent, data):
        if isinstance(data, dict):
            for key, value in data.items():
                item = QTreeWidgetItem(parent)
                item.setText(0, key)
                item.setFlags(item.flags() | Qt.ItemIsTristate)
                if isinstance(value, bool):
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(1, Qt.Checked if value else Qt.Unchecked)
                else:
                    add_items(item, value)
        elif isinstance(data, bool):
            parent.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
            parent.setCheckState(1, Qt.Checked if data else Qt.Unchecked)

    # 트리 초기화
    tree.setHeaderLabels(["항목", "수행 여부"])
    tree.setColumnWidth(0, 300)  # 열 크기 설정
    tree.header().setStretchLastSection(False)  # 마지막 열 자동 확장 비활성화
    tree.itemClicked.connect(handle_item_click)
    # JSON 데이터 추가
    add_items(tree.invisibleRootItem(), json_data)

def handle_item_click(item, column):
    """
    수행 여부의 빈칸 클릭 시 체크박스 상태 변경
    """
    if column == 1:  # 수행 여부 열을 클릭한 경우
        current_state = item.checkState(1)
        new_state = Qt.Checked if current_state == Qt.Unchecked else Qt.Unchecked
        item.setCheckState(1, new_state)

class CustomStyle(QProxyStyle):
    def subElementRect(self, element, option, widget=None):
        rect = super().subElementRect(element, option, widget)
        if element == QStyle.SE_ItemViewItemCheckIndicator:  # 체크박스 크기 설정
            rect.setWidth(100)  # 체크박스 너비
            rect.setHeight(30)  # 체크박스 높이
        return rect

class WrappingItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        """텍스트 줄바꿈을 적용하여 항목 그리기"""
        option.textWrap = True  # 텍스트 줄바꿈 활성화
        super().paint(painter, option, index)

    def sizeHint(self, option, index):
        """항목의 크기 조정 (높이를 늘려 2줄 표시 가능)"""
        size = super().sizeHint(option, index)
        size.setHeight(size.height() * 2)  # 기본 높이를 2배로 늘림
        return size
    
class RealSenseRecorder:
    def __init__(self, output_path, fps, frame_size):
        self.output_path = output_path
        self.fps = fps
        self.frame_size = frame_size
        self.writer = cv2.VideoWriter(
            self.output_path,
            cv2.VideoWriter_fourcc(*'mp4v'),  # 코덱 설정 (예: XVID, MP4V 등)
            self.fps,
            self.frame_size
        )

    def write_frame(self, frame):
        """프레임을 파일로 저장"""
        self.writer.write(frame)

    def close(self):
        """비디오 저장 종료"""
        self.writer.release()

class RealSenseApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI 로드
        loadUi("front.ui", self)
        data=load_json('checkList.json')
        # RealSense Context 초기화
        self.context = rs.context()
        self.devices = []  # 연결된 카메라 목록
        self.views = {}  # 카메라별 View와 Pipeline 관리
        self.timers = {}  # 각 카메라별 QTimer 관리
        self.streaming = False
        self.progress_value=0
        # UI 연결
        self.wholeCheck.stateChanged.connect(self.toggle_all_cameras)
        self.playButton.clicked.connect(self.start_streaming)
        self.outputpathButton.clicked.connect(self.toggle_output_path_load)
        self.cameraList.itemChanged.connect(self.toggle_camera_view)
        self.outputEdit.textChanged.connect(self.toggle_output_path)
        self.cameraList.itemDoubleClicked.connect(self.enable_item_edit) 
        self.checktreeWidget.setStyle(CustomStyle())  # 체크박스 크기 변경
        self.checktreeWidget.setItemDelegate(WrappingItemDelegate())  # 텍스트 줄바꿈 활성화
        self.resetButton.clicked.connect(self.reset_checktree_widget)
        self.saveButton.clicked.connect(self.toggle_checklist_save)
        self.transferButton.clicked.connect(self.toggle_transfer)
        self.LLMButton.clicked.connect(self.toggle_LLM)
        self.speakProgressBar.setValue(self.progress_value)
        self.clearButton.clicked.connect(lambda: self.speakEdit.clear())
        # 녹화 상태
        self.recording = False
        self.recorder = {}
        self.depth_recorder = {}
        self.output_path = "Z:/Workspace/YS_Lee/realsense/data"
        # 녹화 버튼 연결
        self.recordButton.clicked.connect(self.toggle_recording)
        self.outputEdit.setText(self.output_path)
        self.numberEdit.setText("D001")
        populate_tree(self.checktreeWidget,data)
        # 카메라 목록 업데이트
        self.populate_camera_list()
    
    def toggle_LLM(self):
        LLM=gpt_sample.chat()
        if self.speakEdit.toPlainText()=='':
            self.toggle_transfer()
            self.progress_value=75
            self.speakProgressBar.setValue(self.progress_value)
        else:
            self.progress_value=75
            self.speakProgressBar.setValue(self.progress_value)
        response=LLM.response_data(self.speakEdit.toPlainText())
        json_data = json.loads(response)
        self.update_checktree_widget(json_data)
        self.progress_value=100
        self.speakProgressBar.setValue(self.progress_value)
    def update_checktree_widget(self, json_data):
        """checktreeWidget의 항목 상태를 JSON 데이터에 따라 업데이트"""
        def update_items(tree_item, json_data):
            """재귀적으로 트리 항목 업데이트"""
            for i in range(tree_item.childCount()):
                child_item = tree_item.child(i)
                key = child_item.text(0)
                if key in json_data:
                    value = json_data[key]
                    if isinstance(value, bool):
                        # 체크 상태가 비활성화 상태이고 JSON에서 True일 때만 체크
                        if child_item.checkState(1) == Qt.Unchecked and value:
                            child_item.setCheckState(1, Qt.Checked)
                    elif isinstance(value, dict):
                        update_items(child_item, value)

        root = self.checktreeWidget.invisibleRootItem()
        update_items(root, json_data)    
        
    def toggle_transfer(self):
        self.progress_value=25
        self.speakProgressBar.setValue(self.progress_value)
        client = naver_stt.ClovaSpeechClient()
        output_path = os.path.join(self.output_path+'/'+self.numberEdit.text(), 'Voice.m4a' )
        response = client.req_upload(file=output_path , completion='sync')
        if response.status_code == 200:  # 성공적으로 처리된 경우
            response_json = response.json()  # JSON 형식으로 변환
            if 'text' in response_json:  # 'text' 키가 있는지 확인
                self.speakEdit.setText(response_json['text'])  # 텍스트 데이터 출력
            else:
                 self.speakEdit.setText("No text found in response")  # 텍스트 데이터 없음
        else:  # 에러 발생
            self.speakEdit.setText(f"Error occurred: {response.status_code} - {response.text}")
        self.progress_value=50
        self.speakProgressBar.setValue(self.progress_value)
    def reset_checktree_widget(self):
        """checktreeWidget의 모든 체크 상태를 초기화"""
        def reset_items(item):
            """재귀적으로 하위 항목까지 초기화"""
            for i in range(item.childCount()):
                child = item.child(i)
                if child.flags() & Qt.ItemIsUserCheckable:
                    child.setCheckState(1, Qt.Unchecked)  # 체크 해제
                reset_items(child)
        
        root = self.checktreeWidget.invisibleRootItem()
        reset_items(root)
        print("checktreeWidget의 체크 상태가 초기화되었습니다.") 
    def toggle_output_path_load(self):
        """출력 경로를 파일 탐색기를 통해 설정"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",  # 대화 상자 제목
            self.output_path  # 기본 경로
        )
        if directory:  # 사용자가 경로를 선택한 경우
            self.output_path = directory
            self.outputEdit.setText(self.output_path)  # UI 출력 경로 업데이트
            print(f"Output path updated to: {self.output_path}")  
            
    def toggle_checklist_save(self):
        """checktreeWidget의 체크 상태를 JSON 파일로 저장"""
        def extract_checked_states(item):
            """재귀적으로 트리 항목의 체크 상태를 추출"""
            data = {}
            for i in range(item.childCount()):
                child = item.child(i)
                if child.childCount() > 0:
                    # 하위 트리가 존재하는 경우 재귀 호출
                    sub_data = extract_checked_states(child)
                    if sub_data:  # 하위 항목 중 체크된 상태가 있으면 저장
                        data[child.text(0)] = sub_data
                else:
                    # 하위 트리가 없는 경우 체크 상태 저장
                    if child.flags() & Qt.ItemIsUserCheckable:
                        data[child.text(0)] = (child.checkState(1) == Qt.Checked)
            return data

        # 트리의 루트 항목에서 체크 상태 추출
        root = self.checktreeWidget.invisibleRootItem()
        checklist_data = extract_checked_states(root)

        # JSON 파일로 저장
        file_path = "checkList.json"
        create_path(self.output_path+'/'+self.numberEdit.text())
        output_path = os.path.join(self.output_path+'/'+self.numberEdit.text(), file_path )
       
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(checklist_data, file, ensure_ascii=False, indent=2)
        print(f"체크 상태가 {output_path}에 저장되었습니다.")
            
    def toggle_output_path(self):
        """출력 경로 변경"""
        self.output_path = self.outputEdit.text()
        print(f"Output path updated to: {self.output_path}")    
        
    def toggle_recording(self):
        """녹화 시작/중단"""
        if not self.recording:
            print("녹화 시작")
            start_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # 시작 시간 포맷팅
            for i, (device, (camera_view, pipeline)) in enumerate(self.views.items()):
                camera_name = self.cameraList.item(i).text()  # camera_list에서 이름 가져오기
                sanitized_name = camera_name.replace(" ", "_").replace(":", "_")  # 파일명에 적합하도록 변경
                file_name = f"{sanitized_name}_{start_time}_RGB.mp4"  # 이름 + 시간 조합
                create_path(self.output_path+'/'+self.numberEdit.text())
                output_path = os.path.join(self.output_path+'/'+self.numberEdit.text(), file_name)

                self.recorder[device] = RealSenseRecorder(
                    output_path=output_path,
                    fps=30,
                    frame_size=(640, 480)  # 프레임 크기 설정
                )
                if camera_view.show_depth:
                    self.depth_recorder[device] = RealSenseRecorder(
                        output_path=output_path.replace("_RGB.mp4", "_depth.mp4"),
                        fps=30,
                        frame_size=(640, 480)  # 프레임 크기 설정
                    )
                print(f"Recording started for {camera_name}: {output_path}")

            self.recording = True
            self.recordButton.setText("녹화 중단")
        else:
            print("녹화 중단")
            if self.recorder:
                for device in self.recorder.keys():
                    if self.recorder[device] is not None:
                        self.recorder[device].close()
                        print(f"Recording stopped for {device.get_info(rs.camera_info.name)}")
                        self.recorder[device] = None
                for device in self.depth_recorder.keys():
                    if self.depth_recorder[device] is not None:
                        self.depth_recorder[device].close()
                        print(f"Recording stopped for {device.get_info(rs.camera_info.name)}")
                        self.depth_recorder[device] = None
            self.recording = False
            self.recordButton.setText("녹화 시작")
    
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
        if self.recording:
            self.recorder[device].write_frame(copy.deepcopy(color_image))
        # Depth 이미지 업데이트 (USB 3.0인 경우만)
        depth_colormap = None
        if depth_frame:
            depth_image = np.asanyarray(depth_frame.get_data())
            
            depth_colormap = cv2.applyColorMap(
                cv2.convertScaleAbs(depth_image, alpha=0.2), cv2.COLORMAP_JET
            )
            if self.recording:
                depth_3channel = np.stack([cv2.convertScaleAbs(depth_image, alpha=0.2)] * 3, axis=-1) 
                self.depth_recorder[device].write_frame(copy.deepcopy(depth_3channel))
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
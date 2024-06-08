from PyQt5.QtWidgets import QInputDialog, QHBoxLayout, QListWidgetItem, QMessageBox, QLineEdit, QListWidget, \
    QScrollArea, QTextEdit, QApplication, QDesktopWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QSpacerItem, \
    QSizePolicy, QDialog
from PyQt5.QtCore import Qt
from NoticeDetailPage import NoticeDetailPage

class ClickableLabel(QLabel):
    def __init__(self, text="", parent=None, post_id=None):
        super().__init__(text, parent)
        self.parent = parent
        self.post_id = post_id

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.go_to_notice_detail(self.post_id)

class CustomInputDialog(QDialog):
    def __init__(self, current_title="", current_content=""):
        super().__init__()

        self.setWindowTitle("공지 수정")

        # 레이아웃 설정
        layout = QVBoxLayout()

        # 제목 입력 필드
        self.title_label = QLabel("제목:")
        self.title_input = QLineEdit(self)
        self.title_input.setText(current_title)
        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)

        # 내용 입력 필드
        self.content_label = QLabel("내용:")
        self.content_input = QTextEdit(self)
        self.content_input.setText(current_content)
        self.content_input.setFixedHeight(100)  # 내용 입력 필드 높이 조정
        layout.addWidget(self.content_label)
        layout.addWidget(self.content_input)

        # 확인 버튼
        self.ok_button = QPushButton("확인")
        self.ok_button.clicked.connect(self.validate_inputs)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def validate_inputs(self):
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()

        if not title or not content:
            QMessageBox.warning(self, 'Error', '제목과 내용을 모두 입력하세요.')
        else:
            self.accept()

    def getInputs(self):
        return self.title_input.text().strip(), self.content_input.toPlainText().strip()

class NoticePage(QWidget):
    saved_data = {}  # 그룹별 저장된 공지 및 토론 데이터

    def __init__(self, group, main_window, group_id, username):
        super().__init__()
        self.group = group
        self.group_id = group_id
        self.username = username
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        # 여기서 데이터를 읽어와서 하나씩 집어넣음
        self.announcement = self.main_window.get_all_announcement()

        self.layout = QVBoxLayout()

        # 뒤로가기 버튼
        self.back_button = QPushButton('뒤로가기')
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.notice_label = QLabel('공지란')
        self.layout.addWidget(self.notice_label)

        self.notice_input_title = QTextEdit()
        self.notice_input_title.setFixedHeight(30)  # 공지 작성 박스 높이 조정
        self.layout.addWidget(self.notice_input_title)

        self.notice_input_text = QTextEdit()
        self.notice_input_text.setFixedHeight(70)  # 공지 작성 박스 높이 조정
        self.layout.addWidget(self.notice_input_text)

        self.notice_button = QPushButton('공지 작성')
        self.notice_button.clicked.connect(self.add_notice)
        self.layout.addWidget(self.notice_button)

        self.notice_list = QListWidget()
        self.layout.addWidget(self.notice_list)

        # ScrollArea로 감싸기
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        self.show()

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def go_back(self):
        print("back")
        self.main_window.go_back_to_select_page(self.group)

    def add_notice(self):
        notice_title = self.notice_input_title.toPlainText().strip()
        notice_text = self.notice_input_text.toPlainText().strip()
        if notice_title and notice_text:
            self.add_notice_item(notice_title, notice_text)
            self.notice_input_title.clear()
            self.notice_input_text.clear()
        else:
            QMessageBox.warning(self, 'Error', '공지 내용을 입력하세요.')

    def add_notice_item(self, title, text):
        self.main_window.manager.create_announcement(self.main_window.user_id, self.main_window.group_id, title, text)
        self.show()

    def show(self):
        # 기존의 공지 테이블 지우기
        self.notice_list.clear()

        # announcement 정보 가져오기
        announcement = self.main_window.get_all_announcement()

        for i in range(len(announcement)):
            item = QListWidgetItem()
            post_id = announcement[i]['post_id']
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)

            label = ClickableLabel(f"{post_id}. {announcement[i]['post_name']}", self, post_id)
            label.setWordWrap(True)
            layout.setSpacing(10)
            layout.addWidget(label)

            edit_button = QPushButton(f'✎')
            edit_button.setFixedSize(30, 30)
            edit_button.clicked.connect(lambda _, post_id=post_id, label=label: self.edit_notice(post_id, label))
            layout.addWidget(edit_button)

            delete_button = QPushButton(f'✖')
            delete_button.setFixedSize(30, 30)
            delete_button.clicked.connect(lambda _, post_id=post_id: self.delete_notice(post_id))
            layout.addWidget(delete_button)

            widget.setLayout(layout)
            item.setSizeHint(widget.sizeHint())
            self.notice_list.addItem(item)
            self.notice_list.setItemWidget(item, widget)

    def delete_notice(self, post_id):
        self.main_window.manager.delete_announcement(self.main_window.group_id, post_id)
        self.show()

    def edit_notice(self, post_id, label):
        current_title = label.text().split(". ", 1)[1]
        # 여기에 공지 내용도 가져와야 함, 예시로 현재 공지 내용을 빈 문자열로 설정
        current_content = ""  # 실제로는 공지 내용을 가져와야 함

        dialog = CustomInputDialog(current_title, current_content)
        if dialog.exec_() == QDialog.Accepted:
            new_title, new_content = dialog.getInputs()
            if new_title and new_content:
                self.main_window.manager.update_announcement(post_id, new_title, new_content)
                self.show()

    def go_to_notice_detail(self, post_id):
        self.notice_detail_window = NoticeDetailPage(self.main_window, self.group_id, post_id, self.group)
        self.main_window.setCentralWidget(self.notice_detail_window)
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QListWidget, QListWidgetItem, QVBoxLayout, \
    QSpacerItem, QSizePolicy, QPushButton, QLineEdit, QHBoxLayout, QLabel, QGroupBox, QMessageBox
from LoginWindow import *
from GroupSelectPage import GroupSelectPage
from GroupCreatePage import GroupCreatePage


class GroupListPage(QWidget):
    def __init__(self, main_window, username, group_id):
        super().__init__()
        self.username = username
        self.group_id = group_id
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Group List')
        self.setGeometry(100, 100, 400, 500)

        self.layout = QVBoxLayout()
        self.search_layout = QHBoxLayout()
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("그룹 또는 사용자 검색")
        self.search_box.textChanged.connect(self.filter_groups)
        self.search_layout.addWidget(self.search_box)
        if self.main_window.user_type == "professor":
            self.add_button = QPushButton("+", self)
            self.add_button.setFixedSize(30, 30)
            self.add_button.clicked.connect(self.open_group_creat_page)
            self.search_layout.addWidget(self.add_button)

        self.layout.addLayout(self.search_layout)

        # 여기서 데이터 다 읽어오고, 나머지는 기존 코드 활용
        self.groups = self.main_window.get_all_group()

        self.group_boxes = []
        for group in self.groups:
            group_box = self.create_group_box(group)
            self.group_boxes.append(group_box)
            self.layout.addWidget(group_box)

        # 뒤로가기 버튼
        self.back_button = QPushButton('선택 페이지로 돌아가기')
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def create_group_box(self, group):
        group_box = QGroupBox(group['group_name'])
        group_layout = QVBoxLayout()

        info_layout = QHBoxLayout()
        label = QLabel(f"학생 {group['member_count']} 명")
        info_layout.addWidget(label)

        if group['access']:
            visit_button = QPushButton('방문')
            visit_button.clicked.connect(lambda _, g=group: self.visit_group(g))
            info_layout.addWidget(visit_button)
        else:
            lock_button = QPushButton()
            lock_button.setText('🔒')
            lock_button.clicked.connect(lambda _, g=group, gb=group_box: self.toggle_members(g, gb))
            info_layout.addWidget(lock_button)
            
        if self.main_window.user_type == "professor":
            delete_button = QPushButton('delete')
            delete_button.clicked.connect(lambda _, g=group: self.confirm_delete_group(g))
            info_layout.addWidget(delete_button)

        group_layout.addLayout(info_layout)

        members_label = QLabel("\n".join(group['members']))
        members_label.setVisible(False)
        group_layout.addWidget(members_label)

        group_box.setLayout(group_layout)
        group_box.members_label = members_label
        return group_box

    def toggle_members(self, group, group_box):
        members_label = group_box.members_label
        members_label.setVisible(members_label.isVisible() == 0)

    def filter_groups(self):
        search_text = self.search_box.text().lower()
        for i, group in enumerate(self.groups):
            group_box = self.group_boxes[i]
            if search_text in group['group_name'].lower():
                group_box.show()
            else:
                group_box.hide()

    def visit_group(self, group):
        self.group_select_window = GroupSelectPage(group, self.main_window, self.group_id, self.username)
        self.main_window.setCentralWidget(self.group_select_window)
        self.main_window.statusBar().showMessage(group['group_name'] + ' Select Page')
        self.main_window.group_id = group['group_id']

    def open_group_creat_page(self):
        self.group_create_page = GroupCreatePage(self.main_window)
        self.main_window.setCentralWidget(self.group_create_page)
        self.main_window.statusBar().showMessage('Create Group Page')

    def go_back(self):
        self.main_window.go_back_to_origin()

    def confirm_delete_group(self, group):
        reply = QMessageBox.question(self, 'Confirmation', f"그룹 '{group['group_name']}'을(를) 삭제하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.delete_group(group)

    def delete_group(self, group):
        pass

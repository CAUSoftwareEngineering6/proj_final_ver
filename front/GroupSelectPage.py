from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QListWidget, QListWidgetItem, QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton
from LoginWindow import *
from NoticePage import NoticePage
from DebatePage import DebatePage

class GroupSelectPage(QWidget):
    def __init__(self, group, main_window, group_id, username):
        super().__init__()
        self.group = group
        self.group_id = group_id
        self.username = username
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.group['group_name'])
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        notice_button = QPushButton('공지 페이지')
        notice_button.clicked.connect(self.go_to_notice)
        layout.addWidget(notice_button)

        discussion_button = QPushButton('토론 페이지')
        discussion_button.clicked.connect(self.go_to_discussion)
        layout.addWidget(discussion_button)

        back_button = QPushButton('뒤로가기')
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def go_to_notice(self):
        self.notice_window = NoticePage(self.group, self.main_window, self.group_id, self.username)
        self.main_window.setCentralWidget(self.notice_window)

    def go_to_discussion(self):
        self.discussion_window = DebatePage(self.group, self.main_window, self.group_id, self.username)
        self.main_window.setCentralWidget(self.discussion_window)

    def go_back(self):
        self.main_window.go_back_to_group_list()

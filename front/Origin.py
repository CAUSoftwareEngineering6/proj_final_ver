from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QListWidgetItem, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5 import uic
from GroupListPage import *
from UserListPage import *
from LoginWindow import *
from GroupListPage import *

class Origin(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # QPushButton for user list
        self.userListButton = QPushButton("User List", self)
        self.userListButton.clicked.connect(self.open_user_list_page)
        layout.addWidget(self.userListButton)

        self.groupListButton = QPushButton("Group List", self)
        self.groupListButton.clicked.connect(self.open_group_list_page)
        layout.addWidget(self.groupListButton)

        self.BackButton = QPushButton("Back", self)
        self.BackButton.clicked.connect(self.go_back)
        layout.addWidget(self.BackButton)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def open_user_list_page(self):
        self.user_list_page = UserListPage(self.main_window)
        self.main_window.setCentralWidget(self.user_list_page)
        self.main_window.statusBar().showMessage('User List Page')

    def open_group_list_page(self):
        self.group_list_page = GroupListPage(self.main_window, username=self.main_window.username, group_id=self.main_window.group_id)
        self.main_window.setCentralWidget(self.group_list_page)
        self.main_window.statusBar().showMessage('Group List Page')

    def go_back(self):
        self.main_window.go_back_to_login()

from PyQt5.QtWidgets import QMessageBox, QLineEdit, QApplication, QDesktopWidget, QWidget, QListWidget, QListWidgetItem, QVBoxLayout, \
    QHBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from UserDetailPage import UserDetailPage
from UserCreatePage import UserCreatePage


class UserListPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 검색 상자와 + 버튼을 위한 레이아웃
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("사용자 검색")
        # 검색이 시작되면 화면 새로 로딩
        self.search_box.textChanged.connect(self.show)
        search_layout.addWidget(self.search_box)

        
        # + 버튼 추가
        if self.main_window.user_type == "professor":
            self.add_button = QPushButton("+", self)
            self.add_button.setFixedSize(30, 30)
            self.add_button.clicked.connect(self.open_user_creat_page)
            search_layout.addWidget(self.add_button)

        layout.addLayout(search_layout)

        # UserList 를 TableWidget으로 표현
        self.userListWidget = QTableWidget(self)
        if self.main_window.user_type == "professor":
            self.userListWidget.setColumnCount(3)
        else:
            self.userListWidget.setColumnCount(2)
        layout.addWidget(self.userListWidget)

        self.show()

        self.userListWidget.itemClicked.connect(self.open_detail_page)

        # 뒤로가기 버튼
        self.backButton = QPushButton("로그인 페이지로 돌아가기", self)
        self.backButton.clicked.connect(self.go_back)
        layout.addWidget(self.backButton)

        # 공백 구현
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)

    def filter_users(self):
        search_text = self.search_box.text().lower()
        for item in self.user_items:
            item.setHidden(search_text not in item.text().lower())

    def open_detail_page(self):
        # 로직 : 우선 클릭된 셀의 행 값 추출 -> 해당 행의 2번째 값(index=1)의 text추출(학번값) -> 해당 값을 디테일 페이지에 인수로 넘김
        student_id = int(self.userListWidget.item(self.userListWidget.currentRow(), 1).text())
        self.detail_page = UserDetailPage(self.main_window, student_id)
        self.main_window.setCentralWidget(self.detail_page)
        self.main_window.statusBar().showMessage('User Detail Page')

    def go_back(self):
        self.main_window.go_back_to_origin()

    # --------- data 및 출력 관련부 ----------#
    def get_users(self):
        return self.main_window.get_all_user(self.search_box.text() if self.search_box.text() != '' else None)

    def show(self):
        # 기존 테이블 지우기
        self.userListWidget.clear()

        if self.main_window.user_type == "professor":
        # 테이블 열 이름 지정
            self.userListWidget.setHorizontalHeaderLabels(["name", "studentID", "delete"])
        else:
            self.userListWidget.setHorizontalHeaderLabels(["name", "studentID"])

        # 테이블 칸 너비 조절
        self.userListWidget.horizontalHeader().setStretchLastSection(True)

        # 유저 데이터 가져오기
        users = self.get_users()
        print("users in UserList:", users, "\n\n")
        for user in users:
            if user['is_student'] == False:
                users.remove(user)
        print("users in UserList without pro :", users, "\n\n")
        # 행 갯수 지정
        self.userListWidget.setRowCount(len(users))

        # 테이블에 각 데이터 넣기
        for i, user in enumerate(users):
            name = QTableWidgetItem(user['username'])
            student_id = QTableWidgetItem(str(user['personal_id']))
            self.userListWidget.setItem(i, 0, name)
            self.userListWidget.setItem(i, 1, student_id)
            if self.main_window.user_type == "professor":
                delete_button = QPushButton("DELETE")
                delete_button.clicked.connect(lambda _, row=i: self.delete_user(row))
                self.userListWidget.setCellWidget(i, 2, delete_button)

    def delete_user(self, row):
        student_id = self.userListWidget.item(row, 1).text()

        # Display confirmation dialog
        reply = QMessageBox.question(self, 'Confirmation', '삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No,QMessageBox.No)

        # If confirmed, delete the user
        if reply == QMessageBox.Yes:
            self.main_window.delete_user(student_id)
            print(f"delete user with student ID: {student_id}")
            # Show completion message and update the view
            QMessageBox.information(self, 'Deleted', '유저가 삭제되었습니다.')
            self.show()


    def open_user_creat_page(self):
        self.user_create_page = UserCreatePage(self.main_window)
        self.main_window.setCentralWidget(self.user_create_page)
        self.main_window.statusBar().showMessage('User Detail Page')

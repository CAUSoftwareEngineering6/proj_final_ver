from PyQt5.QtWidgets import QTableWidget, QHBoxLayout, QLineEdit, QTextEdit, QApplication, QDesktopWidget, QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy, \
    QPushButton, QListWidget, QListWidgetItem, QTableWidgetItem, QCheckBox, QDialog, QDialogButtonBox, QMessageBox
import sys

class GroupCreatePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 뒤로 가기 버튼
        self.back_Button = QPushButton("뒤로 가기", self)
        self.back_Button.clicked.connect(self.go_back)
        layout.addWidget(self.back_Button)

        # UserList 를 TableWidget으로 표현
        self.userListWidget = QTableWidget(self)
        self.userListWidget.setColumnCount(3)  # 체크박스 열을 위해 3열로 변경
        layout.addWidget(self.userListWidget)

        # create 그룹 버튼
        self.createButton = QPushButton("Creat", self)
        self.createButton.clicked.connect(self.create_group)
        layout.addWidget(self.createButton)

        # 공백 구현
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)
        self.show()

    def create_user(self):
        self.main_window.create_user()
        self.show()

    def go_back(self):
        self.main_window.go_back_to_group_list()

    def create_user(self):
        user_id = self.userid_label.text()
        username = self.username_label.text()
        password = self.password_label.text()
        email = self.email_label.text()
        gender = self.gender_label.text()
        self.main_window.create_user(user_id, username, password, email, gender)
        # 삭제 완료 문구 알림창 뜨고 -> 알림창 확인 클릭시 go_back()호출

    def create_group(self):
        checked_users = []
        for row in range(self.userListWidget.rowCount()):
            checkbox = self.userListWidget.cellWidget(row, 0)
            if checkbox is not None and checkbox.isChecked():
                username_item = self.userListWidget.item(row, 1)
                checked_users.append(username_item.text())
                checkbox.setChecked(False)  # 체크박스를 초기화

        if checked_users:
            print("Checked usernames:", checked_users)
            QMessageBox.information(self, "Success", "그룹이 생성되었습니다!")
        else :
            QMessageBox.information(self, "Fail", "체크를 해주세요!")

    def get_users(self):
        return self.main_window.get_all_user()

    def show(self):
        # 기존 테이블 지우기
        self.userListWidget.clear()

        # 테이블 열 이름 지정
        self.userListWidget.setHorizontalHeaderLabels(["", "name", "studentID"])

        # 테이블 칸 너비 조절
        self.userListWidget.horizontalHeader().setStretchLastSection(True)

        # 유저 데이터 가져오기
        users = self.get_users()

        # 행 갯수 지정
        self.userListWidget.setRowCount(len(users))

        # 테이블에 각 데이터 넣기
        for i, user in enumerate(users):
            checkbox = QCheckBox()
            self.userListWidget.setCellWidget(i, 0, checkbox)
            name = QTableWidgetItem(user['username'])
            student_id = QTableWidgetItem(user['student_id'])
            self.userListWidget.setItem(i, 1, name)
            self.userListWidget.setItem(i, 2, student_id)

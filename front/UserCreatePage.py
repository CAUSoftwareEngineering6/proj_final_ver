from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, QMessageBox

class UserCreatePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('뒤로 가기')
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.go_back_button = QPushButton('뒤로가기')
        self.go_back_button.clicked.connect(self.go_back)
        layout.addWidget(self.go_back_button)

        self.userid_label = QLabel('User id')
        layout.addWidget(self.userid_label)
        self.userid_input = QLineEdit()
        layout.addWidget(self.userid_input)

        self.username_label = QLabel('User name')
        layout.addWidget(self.username_label)
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        self.password_label = QLabel('Password')
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        layout.addWidget(self.password_input)

        self.email_label = QLabel('Eamil')
        layout.addWidget(self.email_label)
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input)

        self.gender_label = QLabel('Gender')
        layout.addWidget(self.gender_label)
        self.gender_input = QLineEdit()
        layout.addWidget(self.gender_input)

        self.create_button = QPushButton('Create')
        self.create_button.clicked.connect(self.create_user)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def create_user(self):
        user_id = self.userid_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()
        gender = self.gender_input.text()
        if not all([user_id, username, password, email, gender]):
            QMessageBox.warning(self, 'Fail', '모든 정보를 기입해주세요!')
        else :
            self.main_window.create_user(user_id, username, password, email, gender)
            QMessageBox.information(self, 'Success', '유저 생성이 완료되었습니다!')
            self.userid_input.clear()
            self.username_input.clear()
            self.password_input.clear()
            self.email_input.clear()
            self.gender_input.clear()
        self.show()

    def go_back(self):
        self.main_window.go_back_to_user_list()

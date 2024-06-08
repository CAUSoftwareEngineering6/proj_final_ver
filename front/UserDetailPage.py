from PyQt5.QtWidgets import QApplication, QDesktopWidget, QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QListWidget, QListWidgetItem

class UserDetailPage(QWidget):
    def __init__(self, main_window, student_id):
        super().__init__()
        self.main_window = main_window
        self.student_id = student_id
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 여기서 데이터 읽어와서 QListWidget에 하나씩 집어넣음(일단 일부만 출력함)
        user = self.main_window.get_detail_user(self.student_id)

        self.userDetailList = QListWidget()

        self.userDetailList.addItems(["user_id :" + user['user_id'],"user_name : "+user['username'],"student_id : "+str(user['student_id'])])
        if user['student_id'] == self.main_window.user_id or self.main_window.user_type == "professor":
            self.userDetailList.addItems(["grade : " + user['grade']])

        layout.addWidget(self.userDetailList)
        
        # QPushButton for back
        self.backButton = QPushButton("Back", self)
        self.backButton.clicked.connect(self.go_back)
        layout.addWidget(self.backButton)

        # Adding a spacer item to the layout
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def go_back(self):
        self.main_window.go_back_to_user_list()


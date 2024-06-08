import sys, os
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QDesktopWidget, QWidget, QListWidgetItem, QVBoxLayout, \
    QSpacerItem, QSizePolicy
from PyQt5 import uic
from Origin import *
from GroupListPage import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from back.Management import Management
from NoticePage import *
from DebatePage import *
from NoticeDetailPage import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.user_id, self.user_name -> login() 뒤에 저장됨
        self.user_id = ''
        self.username = ''
        self.group_id = ''
        self.user_type = ''
        # Management : back과의 의사소통
        self.manager = Management()
        #########################################
        # 메뉴바 예시 -> 사용할 용도가 따로 있으면 사용하는 것도 좋을 것 같습니다.
        # 우선 종료 및 사용자 정보만 간략하게 표시하는 용도로 넣어뒀습니다.
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)

        # file menu action
        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.close)

        # help menu action
        self.name_bar = QAction("이름")
        self.id_bar = QAction("학번/사번")

        # file menu
        file_menu = self.menubar.addMenu("종료")
        file_menu.addAction(self.quit_action)

        # help menu
        help_menu = self.menubar.addMenu("내 정보")
        help_menu.addAction(self.name_bar)
        help_menu.addAction(self.id_bar)
        ##########################################

        ## 최초의 로그인 페이지 열기
        self.login = LoginWindow(self)
        self.setGeometry(100, 100, 300, 150)
        self.center()
        self.setCentralWidget(self.login)
        self.login.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def do_login(self, username, password):
        user = self.manager.login(username, password)
        if user != None:
            print("user:", user)
            self.username = user['username']
            if 'student_id' in user:
                self.user_id = user['student_id']
                self.user_tyep = "student"
                self.group_id = self.manager.get_groups_by_personal_id(self.user_id)
            else:
                self.user_id = user['professor_id']
                self.user_type = "professor"
            self.name_bar.setText(self.username)
            self.id_bar.setText(str(self.user_id))
            return True

        

    # ----------------뒤로 가기 버튼 관련 함수-------------------#
    def go_back_to_login(self):
        self.login = LoginWindow(self)
        self.setGeometry(100, 100, 300, 150)
        self.center()
        self.setCentralWidget(self.login)
        self.statusBar().showMessage('Login Page')

    def go_back_to_origin(self):
        self.origin = Origin(self)
        self.setGeometry(100, 100, 400, 500)
        self.center()
        self.setCentralWidget(self.origin)
        self.statusBar().showMessage('Main Page')

    def go_back_to_user_list(self):
        self.user_list_page = UserListPage(self)
        self.setGeometry(100, 100, 400, 500)
        self.center()
        self.setCentralWidget(self.user_list_page)
        self.statusBar().showMessage('User List Page')

    def go_back_to_group_list(self):
        self.group_list_page = GroupListPage(self, self.username, self.group_id)
        self.setGeometry(100, 100, 400, 500)
        self.center()
        self.setCentralWidget(self.group_list_page)
        self.statusBar().showMessage('Group List Page')

    def go_back_to_select_page(self, group):
        self.group_select_page = GroupSelectPage(group, self, self.group_id, self.username)
        self.setGeometry(100, 100, 400, 500)
        self.center()
        self.setCentralWidget(self.group_select_page)
        #self.statusBar().showMessage(group['name'] + ' Select Page')
    
    def go_back_to_notice_page(self, group):
        self.notice_page = NoticePage(group, self, self.group_id, self.username)
        self.setGeometry(100, 100, 400, 500)
        self.center()
        self.setCentralWidget(self.notice_page)
    
    def go_back_to_debate_page(self, group):
        self.debate_page = DebatePage(group, self, self.group_id, self.username)
        self.setGeometry(100, 100, 400, 500)
        self.center()
        self.setCentralWidget(self.debate_page)


    #-----------데이터 읽어오는 함수------------#
    def get_all_user(self, option=None):
        all_user = self.manager.show_user(searching = option)
        only_students = [d for d in all_user if 'is_student' != False]
        return only_students
    
    def get_all_user_with_professor(self):
        all_user = self.manager.show_user()
        return all_user

    def get_detail_user(self, target_id):
        user = self.manager.show_user_detail(self.user_id, target_id)
        print("detail user", user)
        return user

    def get_all_group(self, option = None):
        all_group = self.manager.show_group(self.user_id, option)
        print(all_group)
        return all_group

    def get_all_announcement(self):
        all_announcement = self.manager.show_announcement(self.group_id)
        print(all_announcement)
        return all_announcement

    def get_all_debate(self):
        all_debate = self.manager.show_debate(self.group_id)
        print(all_debate)
        return all_debate
    
        

    # ---- 유저 생성 및 삭제 ----- #
    def delete_user(self, student_id):
        self.manager.delete_student(student_id)
    
    def create_user(self, user_id: str, username: str, password: str, email: str, gender: str):
        self.manager.create_student(user_id, username, password, email, gender)


    # ---- 그룹 생성 및 삭제 ----- #
    def delete_group(self, group_id):
        self.manager.delete_group(group_id)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

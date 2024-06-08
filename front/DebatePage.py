from PyQt5.QtWidgets import QInputDialog, QHBoxLayout, QListWidgetItem, QMessageBox, QLineEdit, QListWidget, QScrollArea, QTextEdit, QApplication, QDesktopWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy
from ReplyPage import ReplyPage
class DebatePage(QWidget):

    def __init__(self, group, main_window, group_id, username):
        super().__init__()
        self.group = group
        self.group_id = group_id
        self.username = username
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        # 뒤로가기 버튼
        self.back_button = QPushButton('뒤로가기')
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.discussion_label = QLabel('토론란')
        self.layout.addWidget(self.discussion_label)

        self.discussion_input = QLineEdit()
        self.discussion_input.setPlaceholderText('토론 주제 입력')
        self.layout.addWidget(self.discussion_input)

        self.discussion_button = QPushButton('토론 주제 작성')
        self.discussion_button.clicked.connect(self.add_discussion)
        self.layout.addWidget(self.discussion_button)

        self.discussion_list = QListWidget()
        self.layout.addWidget(self.discussion_list)

        # ScrollArea로 감싸기
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_widget.setLayout(self.layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)
        self.load_discussions()

    def go_back(self):
        self.main_window.go_back_to_select_page(self.group)

    def add_discussion(self):
        discussion_text = self.discussion_input.text()
        if discussion_text:
            self.add_discussion_item(discussion_text)
            self.discussion_input.clear()
        else:
            QMessageBox.warning(self, 'Error', '토론 주제를 입력하세요.')

    def add_discussion_item(self, text):
        self.main_window.manager.create_debate(self.main_window.user_id, self.main_window.group_id, text)
        self.load_discussions()

    def load_discussions(self):
        self.discussion_list.clear()

        debate = self.main_window.get_all_debate()

        for i, deb in enumerate(debate):
            item = QListWidgetItem()
            widget = QWidget()
            layout = QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(10)
            post_id = deb['post_id']

            topic_layout = QHBoxLayout()
            topic_label = QLabel(f"{post_id}. {deb['post_name']}")
            topic_label.setWordWrap(True)
            topic_label.mousePressEvent = lambda event, post_id=post_id: self.open_reply_page(post_id)
            topic_layout.addWidget(topic_label)

            edit_button = QPushButton('✎')
            edit_button.setFixedSize(30, 30)
            edit_button.clicked.connect(lambda _, post_id=post_id, label=topic_label: self.edit_discussion(post_id, label))
            topic_layout.addWidget(edit_button)

            delete_button = QPushButton('✖')
            delete_button.setFixedSize(30, 30)
            delete_button.clicked.connect(lambda _, post_id=post_id: self.delete_discussion(post_id))
            topic_layout.addWidget(delete_button)
            layout.addLayout(topic_layout)

            widget.setLayout(layout)
            item.setSizeHint(widget.sizeHint())
            self.discussion_list.addItem(item)
            self.discussion_list.setItemWidget(item, widget)

    def open_reply_page(self, post_id):
        reply_page = ReplyPage(self.group, self.main_window, self.group_id, post_id, self.username)
        self.main_window.setCentralWidget(reply_page)

    def edit_discussion(self, post_id, label):
        current_text = label.text().split(". ", 1)[1]
        text, ok = QInputDialog.getText(self, '토론 수정', '새로운 토론 주제를 입력하세요:', text=current_text)
        if ok and text:
            self.main_window.manager.update_debate(post_id, text)
            self.load_discussions()

    def delete_discussion(self, post_id):
        self.main_window.manager.delete_debate(self.main_window.group_id, post_id)
        self.load_discussions()
from PyQt5.QtWidgets import QInputDialog, QHBoxLayout, QListWidgetItem, QMessageBox, QLineEdit, QListWidget, QScrollArea, QTextEdit, QApplication, QDesktopWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QFrame
from PyQt5.QtCore import Qt

class NoticeDetailPage(QWidget):

    def __init__(self, main_window, group_id, post_id, group):
        super().__init__()
        self.post_id = post_id
        self.group = group
        self.group_id = group_id
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.announcement = self.main_window.get_all_announcement()
        for i in range(len(self.announcement)):
            if self.announcement[i]['post_id'] == self.post_id:
                self.announcement_post_name = self.announcement[i]['post_name']
                self.announcement_post_text = self.announcement[i]['content']

        # 전체 레이아웃
        main_layout = QVBoxLayout()

        # 제목과 내용 프레임
        content_frame = QFrame()
        content_layout = QVBoxLayout()

        # 공지 제목
        self.post_name = QLabel(f"공지 제목")
        self.post_name.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.post_name_text = QLabel(f"{self.announcement_post_name}")
        self.post_name_text.setStyleSheet("background-color: white; border: 1px solid black; padding: 5px;")
        content_layout.addWidget(self.post_name)
        content_layout.addWidget(self.post_name_text)

        # 공지 내용
        self.post = QLabel("공지 내용")
        self.post.setStyleSheet("font-size: 16px;")
        self.post_text = QLabel(f"{self.announcement_post_text}")
        self.post_text.setWordWrap(True)
        self.post_text.setStyleSheet("background-color: white; font-size: 14px; border: 1px solid black; padding: 5px;")
        content_layout.addWidget(self.post)
        content_layout.addWidget(self.post_text)

        content_frame.setLayout(content_layout)
        content_frame.setFrameShape(QFrame.StyledPanel)
        content_frame.setFrameShadow(QFrame.Raised)
        main_layout.addWidget(content_frame)

        # 댓글 레이아웃
        reply_layout = QVBoxLayout()
        reply_layout.setSpacing(10)  # 간격 추가

        self.reply_label = QLabel('댓글')
        reply_layout.addWidget(self.reply_label)

        reply_input_layout = QHBoxLayout()  # 댓글 입력 레이아웃
        self.reply_input = QLineEdit()
        self.reply_input.setPlaceholderText('댓글 입력')
        reply_input_layout.addWidget(self.reply_input)

        self.reply_button = QPushButton('댓글 작성')
        self.reply_button.clicked.connect(self.add_reply)
        reply_input_layout.addWidget(self.reply_button)

        reply_layout.addLayout(reply_input_layout)

        self.reply_list = QListWidget()
        reply_layout.addWidget(self.reply_list)

        main_layout.addLayout(reply_layout)

        # 뒤로가기 버튼 레이아웃
        button_layout = QHBoxLayout()
        self.backButton = QPushButton("Back", self)
        self.backButton.clicked.connect(self.go_back)
        button_layout.addWidget(self.backButton, alignment=Qt.AlignRight)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.load_replies()

    def go_back(self):
        self.main_window.go_back_to_notice_page(self.group)

    def add_reply(self):
        reply_text = self.reply_input.text()
        if reply_text:
            self.add_reply_item(reply_text)
            self.reply_input.clear()
        else:
            QMessageBox.warning(self, 'Error', '댓글 내용을 입력하세요.')

    def load_replies(self):
        self.reply_list.clear()

        announcement = self.main_window.get_all_announcement()
        for ann in announcement:
            if ann['post_id'] == self.post_id:
                for comment in ann['comment_list']:
                    item = QListWidgetItem()
                    comment_id = comment['comment_id']
                    widget = QWidget()
                    comment_layout = QHBoxLayout()
                    comment_layout.setContentsMargins(0, 0, 0, 0)
                    comment_layout.setSpacing(10)

                    reply_label = QLabel(f" - {comment['comment_content']}")
                    reply_label.setWordWrap(True)
                    comment_layout.addWidget(reply_label)

                    edit_button = QPushButton('✎')
                    edit_button.setFixedSize(30, 30)
                    edit_button.clicked.connect(lambda _, post_id=self.post_id, reply_label=reply_label, comment_id=comment_id: self.edit_comment(post_id, reply_label, comment_id))
                    comment_layout.addWidget(edit_button)

                    delete_button = QPushButton('✖')
                    delete_button.setFixedSize(30, 30)
                    delete_button.clicked.connect(
                        lambda _, post_id=self.post_id, comment_id=comment_id: self.delete_comment(post_id, comment_id))
                    comment_layout.addWidget(delete_button)

                    widget.setLayout(comment_layout)
                    item.setSizeHint(widget.sizeHint())
                    self.reply_list.addItem(item)
                    self.reply_list.setItemWidget(item, widget)

    def add_reply_item(self, text):
        self.main_window.manager.create_comment(self.main_window.user_id, self.post_id, text)
        self.load_replies()

    def delete_comment(self, post_id, comment_id):
        self.main_window.manager.delete_comment(comment_id)
        self.load_replies()

    def edit_comment(self, post_id, label, comment_id):
        current_text = label.text().split(' ', 1)[1]
        text, ok = QInputDialog.getText(self, '댓글 수정', '새로운 댓글을 입력하세요:', text=current_text)
        if ok and text:
            self.main_window.manager.update_comment(comment_id, text)
            self.load_replies()

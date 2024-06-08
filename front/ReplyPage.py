from PyQt5.QtWidgets import QInputDialog, QHBoxLayout, QListWidgetItem, QMessageBox, QLineEdit, QListWidget, QScrollArea, QTextEdit, QApplication, QDesktopWidget, QWidget, QLabel, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy


class ReplyPage(QWidget):

    def __init__(self, group, main_window, group_id, post_id, username):
        super().__init__()
        self.group = group
        self.group_id = group_id
        self.post_id = post_id
        self.username = username
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # 뒤로가기 버튼
        self.back_button = QPushButton('뒤로가기')
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.reply_label = QLabel('댓글')
        self.layout.addWidget(self.reply_label)

        self.reply_input = QLineEdit()
        self.reply_input.setPlaceholderText('댓글 입력')
        self.layout.addWidget(self.reply_input)

        self.reply_button = QPushButton('댓글 작성')
        self.reply_button.clicked.connect(self.add_reply)
        self.layout.addWidget(self.reply_button)

        self.reply_list = QListWidget()
        self.layout.addWidget(self.reply_list)

        self.setLayout(self.layout)
        self.load_replies()

    def go_back(self):
        self.main_window.go_back_to_debate_page(self.group)

    def add_reply(self):
        reply_text = self.reply_input.text()
        if reply_text:
            self.add_reply_item(reply_text)
            self.reply_input.clear()
        else:
            QMessageBox.warning(self, 'Error', '댓글 내용을 입력하세요.')

    def load_replies(self):
        self.reply_list.clear()

        debate = self.main_window.get_all_debate()
        for deb in debate:
            if deb['post_id'] == self.post_id:
                for comment in deb['comment_list']:
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
                    edit_button.clicked.connect(lambda _, post_id=self.post_id, reply_label=reply_label,comment_id=comment_id: self.edit_comment(post_id, reply_label,comment_id))
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
        self.main_window.manager.create_comment(self.main_window.user_id,self.post_id, text)
        self.load_replies()

    def delete_comment(self, post_id, comment_id):
        self.main_window.manager.delete_comment(comment_id)
        self.load_replies()

    def edit_comment(self, post_id, label, comment_id):
        current_text = label.text().split(' ', 1)[1]
        text, ok = QInputDialog.getText(self, '답글 수정', '새로운 답글을 입력하세요:', text=current_text)
        if ok and text:
            self.main_window.manager.update_comment(comment_id, text)
            self.load_replies()
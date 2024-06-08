from datetime import datetime

class Comment:
    next_id = 1

    def __init__(self, writer, content: str):
        self.comment_id = str(Comment.next_id)
        Comment.next_id += 1
        self.writer = writer
        self.content = content
        self.created_at = str(datetime.now())
        self.post_id = None

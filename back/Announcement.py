from .Post import Post

class Announcement(Post):
    next_id = 1

    def __init__(self, writer : str, postname: str, content: str):
        super().__init__(writer, postname)
        self.post_id = str(Announcement.next_id)
        Announcement.next_id += 1
        self.content = content

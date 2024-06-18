from .Post import Post
from .User import User
class Debate(Post):
    next_id = 1

    def __init__(self, writer: str, postname: str):
        super().__init__(writer, postname)
        self.post_id = str(Debate.next_id)
        Debate.next_id += 1


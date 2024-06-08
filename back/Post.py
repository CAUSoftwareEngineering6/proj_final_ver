from datetime import datetime
from typing import List
from .Comment import Comment

class Post:

    def __init__(self, writer, postname: str):
        self.writer = writer
        self.postname = postname
        self.comments: List[Comment] = []






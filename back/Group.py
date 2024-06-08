from .User import User
from .Debate import Debate 
from .Announcement import Announcement
from typing import List

class Group:
    next_id = 1

    def __init__(self, group_name: str, professor_id : int):
        self.group_id = Group.next_id
        self.group_name = group_name
        self.professor_id = professor_id
        Group.next_id += 1

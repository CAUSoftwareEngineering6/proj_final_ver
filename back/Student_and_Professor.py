from .User import *
from .Score import *
from typing import List

class Student(User):
    def __init__(self,user_id: str, username: str, password: str, email: str, gender: str, student_id: int, grade: str, score: Score):
        super().__init__(user_id, username, password, email, gender)
        self.student_id = student_id
        self.grade = grade
        self.score = score

class Professor(User):
    def __init__(self, user_id: str, username: str, password: str, email: str, gender: str, professor_id: int, rand: str):
        super().__init__(user_id, username, password, email, gender)
        self.professor_id = professor_id
        self.rand = rand

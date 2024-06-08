from .User import *
from .Score import *
from typing import List

class Student(User):
    def __init__(self,user_id: str, username: str, password: str, email: str, gender: str, student_id: int, grade: str, score: Score):
        super().__init__(user_id, username, password, email, gender)
        self.student_id = student_id
        self.grade = grade
        self.score = score

    def get_grade(self):
        return {
		"attendance": self.score.attendance,
		"midterm" : self.score.midterm,
		"final" : self.score.final,
		"assignment" : self.score.assignment,
		"Whole score" : self.score.calScore()		
	}

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "student_id": self.student_id,
            "grade": self.grade
        })
        return base_dict

    def get_detail(self, current_user_id):
        detail = self.to_dict()
        if current_user_id == self.user_id:
            detail["score"] = {
                "attendance": self.score.attendance,
                "midterm": self.score.midterm,
                "final": self.score.final,
                "assignment": self.score.assignment,
                "whole_score": self.score.calScore()
            }
        return detail

class Professor(User):
    def __init__(self, user_id: str, username: str, password: str, email: str, gender: str, professor_id: int, rand: str):
        super().__init__(user_id, username, password, email, gender)
        self.professor_id = professor_id
        self.rand = rand

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "professor_id": self.professor_id,
            "rand": self.rand
        })
        return base_dict
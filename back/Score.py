class Score:
    def __init__(self, attendance: int, midterm: int, final: int, assignment: int, scoreGrade: str,):
        self.attendance = attendance
        self.midterm = midterm
        self.final = final
        self.assignment = assignment
        self.scoreGrade = scoreGrade
        
        def calScore():
            return attendance+midterm+final+assignment
        
        

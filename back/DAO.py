class messageDAO:
    def __init__(self, db):
        self.db = db

    def create_message(self, sender_id, receiver_id, title, content, date):     ## sender, receiver id 모두 personal_id로 가정하겠습니다.
        max_message_id_query = "SELECT MAX(message_id) FROM MessageBox"
        self.db.query(max_message_id_query)
        max_message_id = self.db.fetchone()[0]
        next_message_id = max_message_id +1 if max_message_id is not None else 1

        query = "INSERT INTO MessageBox (message_id, sender, receiver, title, content, date) VALUES (?, ?, ?, ?, ?, ?)"
        self.db.execute(query, (next_message_id, sender_id, receiver_id, title, content, date))
        return True

    def delete_message(self, message_id):
        query = "DELETE FROM MessageBox WHERE message_id = ?"
        self.db.execute(query, (message_id,))
        return True

    def show_message(self, message_id):
        query = "SELECT sender, receiver, title, content, date FROM MessageBox WHERE message_id = ?"
        self.db.query(query, (message_id,))
        return self.db.fetchone()
    
    def search_message_by_name(self, username):
        result = []
        find_Std_id_query = "SELECT student_id FROM Students where user_id = (SELECT user_id FROM Users where user_id = ?)"
        self.db.query(find_Std_id_query, (username,))
        result.extend(self.db.fetchone())
        find_P_id_query = "SELECT professor_id FROM Professors where user_id = (SELECT user_id FROM Users where user_id = ?)"
        self.db.query(find_P_id_query, (username,))
        result.extend(self.db.fetchone())

    def search_message_by_elseString(self, searching = None):
        result = []
        title_query = "SELECT * FROM MessageBox WHERE title = ?"
        content_query = "SELECT * FROM MessageBox WHERE content = ?"
        date_query = "SELECT * FROM MessageBox WHERE date = ?"
        
        self.db.query(title_query, (searching,))
        result.extend(self.db.fetchone())

        self.db.query(content_query,(searching,))
        result.extend(self.db.fetchone())

        self.db.query(date_query, (searching,))
        result.extend(self.db.fetchone())



class UserDAO:
    def __init__(self, db):
        self.db = db

    def login(self, user_id, password):
        find_user = "SELECT password FROM Users WHERE user_id = ?"
        self.db.query(find_user, (user_id,))
        user_password = self.db.fetchone()
        if user_password is not None:
            if user_password[0] == password:
                find_student_id = "SELECT student_id FROM Students WHERE user_id = ?"
                self.db.query(find_student_id, (user_id,))
                std_id = self.db.fetchone()
                find_professor_id = "SELECT professor_id FROM Professors WHERE user_id = ?"
                self.db.query(find_professor_id, (user_id,))
                pro_id = self.db.fetchone()
                if std_id is None:
                    return self.show_user_detail(pro_id[0], pro_id[0])
                else:
                    return self.show_user_detail(std_id[0], std_id[0])
            else:
                return None

        else:
            return None

    def add_user(self, user):
        query = "INSERT INTO Users (user_id, username, password, email, gender, profileImage) VALUES (?, ?, ?, ?, ?, ?)"
        self.db.execute(query, (user.user_id, user.username, user.password, user.email, user.gender, user.profileImage))

    def add_student(self, user):
        student_id_query = "SELECT MAX(student_id) FROM Students"
        self.db.query(student_id_query)
        max_student_id = self.db.fetchone()[0]
        next_student_id = max_student_id + 1 if max_student_id is not None else 1
            
        score_id_query = "SELECT MAX(score_id) FROM Scores"
        self.db.query(score_id_query)
        max_score_id = self.db.fetchone()[0]
        next_score_id = max_score_id + 1 if max_score_id is not None else 1

        user_query = "INSERT INTO Users (user_id, username, password, email, gender, profileImage) VALUES (?, ?, ?, ?, ?, ?)"
        self.db.execute(user_query, (user.user_id, user.username, user.password, user.email, user.gender, user.profileImage))

        student_query = "INSERT INTO Students (user_id, student_id, grade, score_id) VALUES (?, ?, ?, ?)"
        self.db.execute(student_query, (user.user_id, next_student_id, user.grade,next_score_id))

        score_query = "INSERT INTO Score (score_id, attendance, midterm, final, assignment, scoreGrade VALUES (?, ?, ?, ?, ?, ?)"
        self.db.execute(score_query, (next_score_id, user.score.attendance, user.score.midterm, user.score.final, user.score.assignment, user.score.scoreGrade))

    def get_user(self, user_id):
        query = "SELECT * FROM Users WHERE user_id = ?"
        self.db.query(query, (user_id,))
        return self.db.fetchone()

    def update_user(self, user):
        query = "UPDATE Users SET username = ?, password = ?, email = ?, gender = ?, profileImage = ? WHERE user_id = ?"
        self.db.execute(query, (user.username, user.password, user.email, user.gender, user.profileImage, user.user_id))

    def update_student_score(self, personal_id, score):
        score_id_query = "SELECT score_id FROM Students WHERE student_id = ?"
        self.db.query(score_id_query, (personal_id,))
        score_id = self.db.fetchone()

        update_score_query = "UPDATE Scores SET attendance = ?, midterm = ?, final = ?, assignment = ?, scoreGrade = ?"
        self.db.execute(update_score_query, (score.attendance, score.midterm, score.final, score.assignment, score.scoreGrade))


    def delete_user(self, user_id):
        query = "DELETE FROM Users WHERE user_id = ?"
        self.db.execute(query, (user_id,))

    def delete_student(self, student_id):
        user_id_query = "SELECT user_id FROM Students WHERE student_id = ?"
        self.db.query(user_id_query, (student_id,))
        user_id = self.db.fetchone()

        score_id_query = "SELECT score_id FROM Students WHERE student_id = ?"
        self.db.query(score_id_query, (student_id,))
        score_id = self.db.fetchone()

        delete_user_query = "DELETE FROM Users WHERE user_id = ?"
        delete_student_query = "DELETE FROM Students WHERE student_id = ?"
        delete_score_query = "DELETE FROM Scores WHERE score_id = ?"
        self.db.execute(delete_user_query, (user_id,))
        self.db.execute(delete_student_query, (student_id,))
        self.db.execute(delete_score_query,(score_id,))       

    def get_all_users(self):
        query = "SELECT * FROM Users"
        self.db.query(query)
        return self.db.fetchall()

    def is_student_id(self, student_id):
        query = "SELECT COUNT(*) FROM Students WHERE student_id = ?"
        self.db.query(query, (student_id,))
        count = self.db.fetchone()[0]
        return count > 0
    
    def get_user_by_id(self, personal_id):
        query = """
        SELECT Users.*
        FROM Users
        JOIN Students ON Users.user_id = Students.user_id
        WHERE Students.student_id = ?
        
        UNION
        
        SELECT Users.*
        FROM Users
        JOIN Professors ON Users.user_id = Professors.user_id
        WHERE Professors.professor_id = ?
        """
        self.db.query(query, (personal_id, personal_id))
        return self.db.fetchone()

    def get_user_by_name(self, username):
        query = "SELECT * FROM Users where username = ?"
        self.db.query(query, (username,))
        return self.db.fetchone()  

    # get_user_by_name과 병합 예정
    def get_user_by_personal_id(self, personal_id):
        query = """
        SELECT u.user_id, u.username, u.password, u.email, u.gender, u.profileImage, s.student_id, s.grade, p.professor_id
        FROM Users u
        LEFT JOIN Students s ON u.user_id = s.user_id
        LEFT JOIN Professors p ON u.user_id = p.user_id
        WHERE s.student_id = ? OR p.professor_id = ?
        """
        self.db.query(query, (personal_id, personal_id))
        row = self.db.fetchone()
        if row:
            return {
                'user_id': row[0],
                'username': row[1],
                'password': row[2],
                'email': row[3],
                'gender': row[4],
                'profileImage': row[5],
                'student_id': row[6],
                'grade': row[7],
                'professor_id': row[8]
            }
        return None
    
    def show_user_detail(self, connected_personal_id, finded_personal_id):
        if self.is_student_id(finded_personal_id):
            query = "SELECT Users.user_id, Users.username, Users.password, Users.email, Users.gender, Users.profileImage, Students.student_id, Students.grade, Scores.attendance, Scores.midterm, Scores.final, Scores.assignment, Scores.scoreGrade FROM Users JOIN Students ON Users.user_id = Students.user_id JOIN Scores ON Students.score_id = Scores.score_id WHERE Students.student_id = ?"
            self.db.query(query, (finded_personal_id,))
            finded_user = self.db.fetchone()
            if self.is_student_id(connected_personal_id):
                if finded_personal_id == connected_personal_id:
                    return {
                    "user_id": finded_user[0],
                    "username": finded_user[1],
                    "password": finded_user[2],
                    "email": finded_user[3],
                    "gender": finded_user[4],
                    "profileImage": finded_user[5],
                    "student_id": finded_user[6],
                    "grade": finded_user[7],
                    "attendance": finded_user[8],
                    "midterm": finded_user[9],
                    "final": finded_user[10],
                    "assignment": finded_user[11],
                    "scoreGrade": finded_user[12]
                }
                else:
                    return {
                    "user_id": finded_user[0],
                    "username": finded_user[1],
                    "password": finded_user[2],
                    "email": finded_user[3],
                    "gender": finded_user[4],
                    "profileImage": finded_user[5],
                    "student_id": finded_user[6],
                    "grade": finded_user[7]
                }
            else:
                return {
                    "user_id": finded_user[0],
                    "username": finded_user[1],
                    "password": finded_user[2],
                    "email": finded_user[3],
                    "gender": finded_user[4],
                    "profileImage": finded_user[5],
                    "student_id": finded_user[6],
                    "grade": finded_user[7],
                    "attendance": finded_user[8],
                    "midterm": finded_user[9],
                    "final": finded_user[10],
                    "assignment": finded_user[11],
                    "scoreGrade": finded_user[12]
                }
        else:
            query = "SELECT Users.user_id, Users.username, Users.password, Users.email, Users.gender, Users.profileImage, Professors.professor_id, Professors.rand FROM Users JOIN Professors ON Users.user_id = Professors.user_id WHERE Professors.professor_id = ?"
            self.db.query(query, (finded_personal_id,))
            finded_user = self.db.fetchone()
            return {
                "user_id": finded_user[0],
                "username": finded_user[1],
                "password": finded_user[2],
                "email": finded_user[3],
                "gender": finded_user[4],
                "profileImage": finded_user[5],
                "professor_id": finded_user[6],
                "rand": finded_user[7]
        }
        
    def get_student_by_user_id(self, user_id):
        query = "SELECT * FROM Students WHERE user_id = ?"
        self.db.query(query, (user_id,))
        return self.db.fetchone()


    def get_professor_by_user_id(self, user_id):
        query = "SELECT * FROM Professors WHERE user_id = ?"
        self.db.query(query, (user_id,))
        return self.db.fetchone()



class GroupDAO:
    def __init__(self, db):
        self.db = db

    def create_group(self, group):
        try:
            # 그룹 생성
            query = "INSERT INTO CAUGroups (group_name) VALUES (?)"
            self.db.execute(query, (group.group_name,))
            group_id = self.db.lastrowid()

            # 그룹 생성자가 멤버로 자동 추가
            self.add_member_to_group(group_id, group.professor_id)
            return group_id
        except Exception as e:
            print(f"Error creating group: {e}")
            return None

    def get_group(self, group_id):
        query = "SELECT * FROM CAUGroups WHERE group_id = ?"
        self.db.query(query, (group_id,))
        return self.db.fetchone()

    def update_group(self, group):
        query = "UPDATE CAUGroups SET group_name = ? WHERE group_id = ?"
        self.db.execute(query, (group.group_name, group.group_id))

    def delete_group(self, group_id):
        query = "DELETE FROM CAUGroups WHERE group_id = ?"
        self.db.execute(query, (group_id,))

    def get_all_groups(self):
        query = "SELECT * FROM CAUGroups"
        self.db.query(query)
        groups = self.db.fetchall()
        # 튜플을 딕셔너리로 변환
        return [{"group_id": group[0], "group_name": group[1]} for group in groups]


    def get_group_by_name(self, group_name):
        query = "SELECT * FROM CAUGroups WHERE group_name LIKE ?"
        self.db.query(query, ('%' + group_name + '%',))
        groups = self.db.fetchall()
        # 튜플을 딕셔너리로 변환
        return [{"group_id": group[0], "group_name": group[1]} for group in groups]


    def get_groups_by_member_name(self, member_name):
        query = """
        SELECT g.group_id, g.group_name FROM CAUGroups g
        JOIN GroupMembers gm ON g.group_id = gm.group_id
        JOIN Students s ON gm.personal_id = s.student_id
        JOIN Users u ON s.user_id = u.user_id
        WHERE u.username LIKE ?
        """
        self.db.query(query, ('%' + member_name + '%',))
        groups = self.db.fetchall()
        return [{"group_id": group[0], "group_name": group[1]} for group in groups]

    def get_group_with_members(self, group_id):
        group_query = "SELECT * FROM CAUGroups WHERE group_id = ?"
        self.db.query(group_query, (group_id,))
        group_data = self.db.fetchone()

        if group_data:
            group = {
                "group_id": group_data[0],
                "group_name": group_data[1],
                "members": []
            }

            # 멤버 이름만 가져오기
            members_query = """
            SELECT u.username FROM Users u
            JOIN Students s ON u.user_id = s.user_id
            JOIN GroupMembers gm ON s.student_id = gm.personal_id
            WHERE gm.group_id = ?
            """
            self.db.query(members_query, (group_id,))
            members_data = self.db.fetchall()

            # 디버깅 출력을 추가하여 데이터 확인

            for member_data in members_data:
                group["members"].append(member_data[0])  # 멤버 이름 추가

            group["member_count"] = len(group["members"])
            return group
        return None
    def check_user_access(self, group_id, personal_id):
        members_query = """
        SELECT 1 FROM GroupMembers gm
        WHERE gm.group_id = ? AND gm.personal_id = ?
        """
        self.db.query(members_query, (group_id, personal_id))
        return self.db.fetchone() is not None
    def check_user_access(self, group_id, personal_id):
        members_query = """
        SELECT 1 FROM GroupMembers gm
        WHERE gm.group_id = ? AND gm.personal_id = ?
        """
        self.db.query(members_query, (group_id, personal_id))
        return self.db.fetchone() is not None

    def add_member_to_group(self, group_id, student_id):
        query = "INSERT INTO GroupMembers (group_id, personal_id) VALUES (?, ?)"
        self.db.execute(query, (group_id, student_id))


    def delete_member_from_group(self, group_id, student_id):
        query = "DELETE FROM GroupMembers WHERE group_id = ? AND personal_id = ?"
        self.db.execute(query, (group_id, student_id))

    def add_post_to_group(self, group_id, post_id):
        query = "INSERT INTO GroupPosts (group_id, post_id) VALUES (?, ?)"
        self.db.execute(query, (group_id, post_id))

    def remove_post_from_group(self, group_id, post_id):
        query = "DELETE FROM GroupPosts WHERE group_id = ? AND post_id = ?"
        self.db.execute(query, (group_id, post_id))


class PostDAO:
    def __init__(self, db):
        self.db = db

    def get_post_by_id(self, post_id):
        query = "SELECT * FROM Posts WHERE post_id = ?"
        self.db.query(query, (post_id,))
        row = self.db.fetchone()
        if row:
            return {
                "post_id": row[0],
                "personal_id": row[1],
                "postname": row[2],
                "created_at": row[3],
                "type": row[4],
                "content": row[5]
            }
        return None

    def add_post(self, personal_id, postname, type, content=None):
        query = "INSERT INTO Posts (personal_id, postname, created_at, type, content) VALUES (?, ?, datetime('now'), ?, ?)"
        self.db.execute(query, (personal_id, postname, type, content))
        return self.db.lastrowid()

    def add_debate(self, debate):
        return self.add_post(debate.writer, debate.postname, 'debate')

    def add_announcement(self, announcement):
        return self.add_post(announcement.writer, announcement.postname, 'announcement', announcement.content)

    def update_post(self, post_id, postname, content=None):
        query = "UPDATE Posts SET postname = ?, content = ? WHERE post_id = ?"
        self.db.execute(query, (postname, content, post_id))

    def delete_post(self, post_id):
        query = "DELETE FROM Posts WHERE post_id = ?"
        self.db.execute(query, (post_id,))

    def get_posts_by_group_and_type(self, group_id, type):
        query = """
        SELECT p.post_id, p.postname, p.content, p.created_at, u.username
        FROM GroupPosts gp
        JOIN Posts p ON gp.post_id = p.post_id
        LEFT JOIN Students s ON p.personal_id = s.student_id
        LEFT JOIN Professors pr ON p.personal_id = pr.professor_id
        LEFT JOIN Users u ON u.user_id = COALESCE(s.user_id, pr.user_id)
        WHERE gp.group_id = ? AND p.type = ?
        """
        self.db.query(query, (group_id, type))
        return self.db.fetchall()


class CommentDAO:
    def __init__(self, db):
        self.db = db

    def add_comment(self, comment):
        query = "INSERT INTO Comments (writer_id, post_id, content, created_at) VALUES (?, ?, ?, datetime('now'))"
        self.db.execute(query, (comment.writer, comment.post_id, comment.content))

    def get_comment(self, comment_id):
        query = "SELECT * FROM Comments WHERE comment_id = ?"
        self.db.query(query, (comment_id,))
        return self.db.fetchone()

    def delete_comment(self, comment_id):
        query = "DELETE FROM Comments WHERE comment_id = ?"
        self.db.execute(query, (comment_id,))

    def update_comment(self, comment_id, new_content):
        query = "UPDATE Comments SET content = ? WHERE comment_id = ?"
        self.db.execute(query, (new_content, comment_id))

    def get_comments_by_post(self, post_id):
        query = """
        SELECT c.comment_id, c.writer_id, c.content, c.created_at
        FROM Comments c
        WHERE c.post_id = ?
        """
        self.db.query(query, (post_id,))
        return self.db.fetchall()
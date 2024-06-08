# Management.py
from .DAO import *
from .database import Database
from .User import User
from .Group import Group
from .Debate import Debate
from .Announcement import Announcement
from .Comment import Comment
from .Student_and_Professor import *
from .Score import *

class Management:
    def __init__(self, db_path='SWE.db'):
        self.db = Database(db_path)
        self.message_dao = messageDAO(self.db)
        self.user_dao = UserDAO(self.db)
        self.group_dao = GroupDAO(self.db)
        self.comment_dao = CommentDAO(self.db)
        self.post_dao = PostDAO(self.db)

    def login(self, user_id, password):
        return self.user_dao.login(user_id, password)

    def get_user(self, user_id):
        return self.user_dao.get_user(user_id)

    def create_user(self, user_id, username, password, email, gender):
        new_user = User(user_id, username, password, email, gender)
        self.user_dao.add_user(new_user)
        return True
    
    def create_student(self, user_id, username, password, email, gender, student_id, grade, attendance, midterm, final, assignment, scoreGrade):
        new_student = Student(user_id, username, password, email, gender, student_id, grade, Score(attendance, midterm, final, assignment, scoreGrade))

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        if user:
            self.user_dao.delete_user(user_id)
            return True
        return False
    
    def delete_student(self, student_id):
        self.user_dao.delete_student(student_id)
        return True

    def update_user(self, user_id, username, password, email, gender, profileImage):
        user = self.get_user(user_id)
        if user:
            user.username = username
            user.password = password
            user.email = email
            user.gender = gender
            user.profileImage = profileImage
            self.user_dao.update_user(user)
            return True
        return False
    
    def update_student_score(self, student_id, attendance, midterm, final, assignment, scoreGrade):
        new_score = Score(attendance, midterm, final, assignment, scoreGrade)
        self.user_dao.update_student_score(student_id, new_score)
        return True
    
    def get_user_by_name(self, username):
        return self.user_dao.get_user_by_name(username)

    def get_user_by_id(self, personal_id):
        return self.user_dao.get_user_by_id(personal_id)
    
    def show_user(self, searching=None):
        def to_dict(user, personal_id=None, is_student=None):
            return {
                "user_id": user[0],
                "username": user[1],
                "password": user[2],
                "email": user[3],
                "gender": user[4],
                "profileImage": user[5],
                "personal_id": personal_id,
                "is_student": is_student
            }

        result = []
        if searching is None:
            users = self.user_dao.get_all_users()
            for user in users:
                student = self.user_dao.get_student_by_user_id(user[0])
                professor = self.user_dao.get_professor_by_user_id(user[0])
                if student:
                    result.append(to_dict(user, student[1], True))
                elif professor:
                    result.append(to_dict(user, professor[1], False))
                else:
                    result.append(to_dict(user))
        else:
            by_id = self.user_dao.get_user_by_id(searching)
            if by_id:
                student = self.user_dao.get_student_by_user_id(searching)
                professor = self.user_dao.get_professor_by_user_id(searching)
                if student:
                    result.append(to_dict(by_id, student[1], True))
                elif professor:
                    result.append(to_dict(by_id, professor[1], False))
                else:
                    result.append(to_dict(by_id))
            by_name = self.user_dao.get_user_by_name(searching)
            if by_name:
                for user in by_name:
                    student = self.user_dao.get_student_by_user_id(user[0])
                    professor = self.user_dao.get_professor_by_user_id(user[0])
                    if student:
                        result.append(to_dict(user, student[1], True))
                    elif professor:
                        result.append(to_dict(user, professor[1], False))
                    else:
                        result.append(to_dict(user))

        return result
        
    def show_user_detail(self, connected_personal_id, finded_personal_id):
        return self.user_dao.show_user_detail(connected_personal_id, finded_personal_id)

# ---------------------메시지 기능----------------------------------------

    def create_message(self, sender_personal_id, receiver_personal_id, title, content, date):
        return self.message_dao.create_message(sender_personal_id, receiver_personal_id, title, content, date)

    def delete_message(self, message_id):
        return self.message_dao.delete_message(message_id)
    
    def show_message(self, message_id):
        return self.message_dao.show_message(message_id)
    
    def search_message(self, searching = None):
        result = []
        result.append(self.message_dao.search_message_by_name(searching))
        result.append(self.message_dao.search_message_by_elseString(searching))
        return result



# ----------------------그룹 기능 ----------------------------------------
    def get_groups_by_personal_id(self, personal_id):
        query = """
        SELECT gm.group_id FROM GroupMembers gm
        WHERE gm.personal_id = ?
        """
        self.db.query(query, (personal_id,))
        group_ids = self.db.fetchall()
        return [group_id[0] for group_id in group_ids]

    def show_group(self, personal_id, searching=None):
        result = []

        if searching is None:
            groups = self.group_dao.get_all_groups()
            for group in groups:
                group_with_members = self.group_dao.get_group_with_members(group['group_id'])
                if group_with_members:
                    group_with_members['access'] = self.group_dao.check_user_access(group['group_id'], personal_id)
                    result.append(group_with_members)
        else:
            # 멤버 이름으로 검색
            by_member_name = self.group_dao.get_groups_by_member_name(searching)
            for group in by_member_name:
                group_with_members = self.group_dao.get_group_with_members(group['group_id'])
                if group_with_members:
                    group_with_members['access'] = self.group_dao.check_user_access(group['group_id'], personal_id)
                    result.append(group_with_members)

            # 그룹 이름으로 검색
            by_name = self.group_dao.get_group_by_name(searching)
            for group in by_name:
                group_with_members = self.group_dao.get_group_with_members(group['group_id'])
                if group_with_members:
                    group_with_members['access'] = self.group_dao.check_user_access(group['group_id'], personal_id)
                    result.append(group_with_members)

        return result

    def create_group(self, group_name, professor_id):
        new_group = Group(group_name, professor_id)
        group_id = self.group_dao.create_group(new_group)
        return group_id is not None

    def delete_group(self, group_id):
        group = self.group_dao.get_group(group_id)
        if group:
            self.group_dao.delete_group(group_id)
            return True
        return False

    def add_member_to_group(self, group_id, student_id):
        group = self.group_dao.get_group(group_id)
        student = self.user_dao.get_user_by_personal_id(student_id)
        print(student)
        print(group)
        if group and student:
            self.group_dao.add_member_to_group(group_id, student_id)
            return True
        return False

    def delete_member_from_group(self, group_id, student_id):
        group = self.group_dao.get_group(group_id)
        student = self.user_dao.get_user_by_personal_id(student_id)
        if group and student:
            self.group_dao.delete_member_from_group(group_id, student_id)
            return True
        return False

    def show_debate(self, group_id):
        posts = self.post_dao.get_posts_by_group_and_type(group_id, 'debate')
        post_list = []
        for post in posts:
            post_id, postname, content, created_at, username = post
            comment_list = self.get_comments_by_post(post_id)
            post_list.append({
                'post_id': post_id,
                'writer_name': username,
                'post_name': postname,
                'comment_list': comment_list,
                'created_at': created_at
            })
        return post_list

    def show_announcement(self, group_id):
        posts = self.post_dao.get_posts_by_group_and_type(group_id, 'announcement')
        post_list = []
        for post in posts:
            post_id, postname, content, created_at, username = post
            comment_list = self.get_comments_by_post(post_id)
            post_list.append({
                'post_id': post_id,
                'writer_name': username,
                'post_name': postname,
                'content': content,
                'comment_list': comment_list,
                'created_at': created_at
            })
        return post_list

    def create_debate(self, personal_id, group_id, postname):
        user = self.user_dao.get_user_by_personal_id(personal_id)
        if user:
            new_debate = Debate(personal_id, postname)
            new_post_id = self.post_dao.add_debate(new_debate)
            self.group_dao.add_post_to_group(group_id, new_post_id)
            return True
        return False

    def create_announcement(self, personal_id, group_id, postname, content):
        user = self.user_dao.get_user_by_personal_id(personal_id)
        if user:
            new_announcement = Announcement(personal_id, postname, content)
            new_post_id = self.post_dao.add_announcement(new_announcement)
            self.group_dao.add_post_to_group(group_id, new_post_id)
            return True
        return False

    def delete_debate(self, group_id, post_id):
        post = self.post_dao.get_post_by_id(post_id)
        if post and post['type'] == 'debate':
            self.post_dao.delete_post(post_id)
            self.group_dao.remove_post_from_group(group_id, post_id)
            return True
        return False

    def delete_announcement(self, group_id, post_id):
        post = self.post_dao.get_post_by_id(post_id)
        if post and post['type'] == 'announcement':
            self.post_dao.delete_post(post_id)
            self.group_dao.remove_post_from_group(group_id, post_id)
            return True
        return False

    def update_debate(self, post_id, postname):
        post = self.post_dao.get_post_by_id(post_id)
        if post and post['type'] == 'debate':
            self.post_dao.update_post(post_id, postname, None)
            return True
        return False

    def update_announcement(self, post_id, postname, content):
        post = self.post_dao.get_post_by_id(post_id)
        if post and post['type'] == 'announcement':
            self.post_dao.update_post(post_id, postname, content)
            return True
        return False

    def show_debate(self, group_id):
        posts = self.post_dao.get_posts_by_group_and_type(group_id, 'debate')
        post_list = []
        for post in posts:
            post_id, postname, content, created_at, username = post
            comment_list = self.get_comments_by_post(post_id)
            post_list.append({
                'post_id': post_id,
                'writer_name': username,
                'post_name': postname,
                'comment_list': comment_list,
                'created_at': created_at
            })
        return post_list

    def show_announcement(self, group_id):
        posts = self.post_dao.get_posts_by_group_and_type(group_id, 'announcement')
        post_list = []
        for post in posts:
            post_id, postname, content, created_at, username = post
            comment_list = self.get_comments_by_post(post_id)
            post_list.append({
                'post_id': post_id,
                'writer_name': username,
                'post_name': postname,
                'content': content,
                'comment_list': comment_list,
                'created_at': created_at
            })
        return post_list


    def create_comment(self, personal_id, post_id, content):
        user = self.user_dao.get_user_by_personal_id(personal_id)
        if user:
            new_comment = Comment(user['username'], content)
            new_comment.post_id = post_id
            self.comment_dao.add_comment(new_comment)
            return True
        return False

    def delete_comment(self, comment_id):
        comment = self.comment_dao.get_comment(comment_id)
        if comment:
            self.comment_dao.delete_comment(comment_id)
            return True
        return False


    def update_comment(self, comment_id, new_content):
        comment = self.comment_dao.get_comment(comment_id)
        if comment:
            self.comment_dao.update_comment(comment_id, new_content)
            return True
        return False

    def get_comments_by_post(self, post_id):
        comments = self.comment_dao.get_comments_by_post(post_id)
        comment_list = []
        for comment in comments:
            comment_id, username, content, created_at = comment
            comment_list.append({
                'comment_id': comment_id,
                'comment_username': username,
                'comment_content': content,
                'created_at': created_at
            })
        return comment_list

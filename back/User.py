
class User:
    def __init__(self,user_id: str, username: str, password: str, email: str, gender: str):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.gender = gender
        self.profileImage = '프로필 대표 이미지(url)'
#        self.messageBox = messageBox

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "gender": self.gender,
            "profileImage": self.profileImage
        }

    def update_Password(self, new_password: str):
        self.password = new_password
        return True

    def updateProfileImage(self):
        pass

    def update_Email(self, new_email: str):
        self.email = new_email
        return True

    def sendMessage(self):
        pass

    def showMessage(self):
        pass

    # 아래부분은 그냥 Mangement에서 구현하면 될듯하여 우선 주석처리 했습니다!

    # def create_debate(self, group_id: int, postname: str, management:management):
	# return management.create_debate(self.user_id, group_id, postname)
    #
    # def update_debate(self, group_id: int, content: str, management:management):
	# return management.update_debate(self.user_id, group_id, postname)
    #
    # def create_comment(self, group_id: int, post_id : int, content:str, management:management):
	# return management.create_announcement_comment(self.user_id, group_id, post_id, , content)
    #
    # def search_user_by_name(self, user_name: str, management: Management):
    #     return management.get_user_by_name(user_name)
    #
    # def search_user_by_id(self, personal_id: int, management: Management):
    #     return management.get_user_by_id(personal_id)
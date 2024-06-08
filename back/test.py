from .Management import Management

M = Management()

# searching에 인자가 있는 경우에는 구현하지 못함
# print('show_user 테스트')
# print(M.show_user())
# #
# print('show_user 이름 검색 테스트')
# print(M.show_user('이름1'))
# #
# print('show_user 학번 검색 테스트')
# print(M.show_user('103'))
# #
# print('get_user 테스트')
# print(M.get_user('user2'))
#
# print('\ncreate_user 테스트')
# M.create_user("5", "user5", "1234", "user5@cau.ac.kr", "female")
# print(M.show_user())
#
# print('\ndelete_user 테스트')
# M.delete_user("4")
# print(M.show_user())
#
# print('\nshow_user_detail 테스트: 1 자기 자신 2 다른 사람')
# print(M.show_user_detail("101","101"))
# print(M.show_user_detail("101","102"))
#
# print('\nshow_user_detail 테스트 2 (교수): 1 자기 자신 2 다른 사람')
# print(M.show_user_detail("201","101"))
# print(M.show_user_detail("201","201"))



# ----------------------- 그룹 테스트 -------------------
# print('show_group 테스트(인자 X)')
# print(M.show_group(201))
# #
# print('show_group 테스트(그룹 이름)')
# print(M.show_group(101, 'Group 1'))
#
# print('show_group 테스트(학생 이름)')
# print(M.show_group(101, '이름3'))

# print('delete group test 테스트')
# print(M.delete_group(8))
#
# print('create group test 테스트')
# M.create_group("Group 3", 201)
# print(M.show_group(201))



#
# print('add_member_to_group test 테스트')
# print(M.add_member_to_group(9, 101))
# print(M.show_group(103, 'Group 3'))
#
# print('delete_member_from_group test 테스트')
# M.delete_member_from_group(9, 101)
# print(M.show_group(103, 'Group 3'))

# print('show_debate 테스트')
# print(M.show_debate(1))
# print('show_announcement 테스트')
# print(M.show_announcement(1))

# print('create_debate 테스트')
# print(M.create_debate(101, 2, '새로운 토론'))
# print(M.show_debate(2))
#
# print('create_announcement 테스트')
# print(M.create_announcement(201, 2, '새로운 공지', '공지내용'))
# print(M.show_announcement(2))
#
# print('delete_debate 테스트')
# print(M.show_debate(2))
# print(M.delete_debate(2, 5))
# print(M.show_debate(2))
#
# print('delete_announcement 테스트')
# print(M.show_announcement(2))
# print(M.delete_announcement(2, 6))
# print(M.show_announcement(2))
#
# print('update_debate 테스트')
# print(M.show_debate(1))
# print(M.update_debate(1, "갱신된 토론 제목"))
# print(M.show_debate(1))
#
# print('update_announcement 테스트')
# print(M.show_announcement(1))
# print(M.update_announcement(2, "갱신된 공지 제목", "갱신된 공지 내용"))
# print(M.show_announcement(1))


# print('create_comment 테스트')
# print(M.show_announcement(1))
# print(M.create_comment(101, 2, "생성된 댓글 내용"))
# print(M.show_announcement(1))


# print('delete_comment 테스트')
# print(M.show_announcement(1))
# print(M.delete_comment(4))
# print(M.show_announcement(1))


# print('delete_comment 테스트')
# print(M.show_announcement(1))
# print(M.update_comment(3, '갱신된 댓글 내용'))
# print(M.show_announcement(1))
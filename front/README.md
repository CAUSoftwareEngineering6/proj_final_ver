# frontend_1

<구조>
MainWindow
	ㄴOrigin
	   ㄴGroupListPage
	  	ㄴGroupDetailPage
	   ㄴUserListPage
		ㄴUserDetailPage

<실행>
python MainWindow.py

<특이사항>
MainWindow를 QMainWindow객체로 지정하고, 해당 객체에서 setCentralWidget()으로
특정 위젯을 화면에 띄우고, 뒤로가기 버튼을 구현하니까 이전 위젯의 객체가 삭제되어 메모리 참조 에러가 발생했습니다.

그래서 구조도에서 보듯이 Origin(QWidget)을 그룹리스트와 유저리스트로 가기 위한 중간 위젯으로 설정해서 구현했습니다.

test.py <- 상단메뉴 탭 테스트

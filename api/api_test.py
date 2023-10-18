import function as f

# 1. 게임 생성
# 게임 초기 선택지들 입력받기 => 나중에 선택한 키워드가 들어오도록 바꾸기
background = input("배경 선택: ")
mood = input("분위기: ")
player_name = input("플레이어 이름: ")

# 마을 이름 생성
town = f.getTownName(background, mood, player_name)
# 마을 배경 설명
f.getTownBackground(town, background, mood)
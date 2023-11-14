import gpt_function as gpt
import intro_function as intro
import npc_function as npc
import objective_function as obj
import const as c

# 1. 게임 생성
# 게임 초기 선택지들 입력받기 => 나중에 선택한 키워드가 들어오도록 바꾸기
background = input("배경 선택: ")
genre = input("장르: ")
player_name = input("플레이어 이름: ")

# 마을 이름 생성
town = intro.getTownName(background, genre, player_name)
# 마을 배경 설명
town_detail = intro.getTownBackground(town, background, genre)
# 게임 목표 설정
game_objective, game_objective_summary = obj.setGameObjective(town=town, town_detail=town_detail,genre=genre,background=background)
game_objective_done = []
for obj in game_objective:  # 게임 목표 달성도 초기화
    game_objective_done.append(False)
# NPC 생성
#NPC_name = npc.getNPCName(background, genre)
#NPC_info = npc.getNPCInfo(town, NPC_name)

# 2. 게임 시작
# 시스템 설정 - 데이터 적재용
system_intro = c.SYSTEM_INTRO

query = "마을 이름은 " + town + "이고, 플레이어 이름은 " + player_name + "이야. NPC 이름은 " #+ \
    #NPC_name + "이고," + NPC_name + "은 " + NPC_info + "처럼 행동해야 해"
query += background + " 배경의 " + genre + " 분위기의 TRPG 스크립트 생성"

messages = [
    {"role": "system", "content": system_intro},
    {"role": "user", "content": query}
]

final_objective = 0
curr_objective = 1


# 중간 목표 달성 여부 체크
system_objective_checker = '''당신은 입력된 스크립트 내용에서 주어진 게임의 목표 달성 여부를 확인하는 objective checker이다. 
출력은 오로지 "True" 혹은 "False" 로만 한다. 
현재 플레이어의 목표는 '''+game_objective[curr_objective]+'''이고 목표에 대한 설명은 다음과 같다.
'''+game_objective_summary[curr_objective]


system_play = c.SYSTEM_PLAY

# 반복문 돌면서 API 호출
while (True):
    # ChatGPT API 호출
    response = gpt.callGPT(messages=messages, stream=True)

    # 시스템 설정 수정
    messages[0] = {"role": "system", "content": system_play}

    # 이전 턴 요약 후 저장 => 2개만
    print("처리중...")
    response = gpt.summary(response=response)
    messages.append(
        {"role": "assistant", "content": response}
    )

    # 목표 달성 여부 체크
    messages_objective = [
        {"role": "system", "content": system_objective_checker},
    ]
    
    messages_objective.append(messages[len(messages)-1])
        
    print("현재 목표:"+str(curr_objective)+"\n"+game_objective[curr_objective]+"\n목표 달성 여부:")
    response = gpt.callGPT(messages=messages_objective,stream=True)

    if(response == "True"):
        if(curr_objective<len(game_objective)-1):
            curr_objective+=1
        elif(curr_objective==0):
            print("게임 종료")
        elif(curr_objective==4):
            curr_objective = 0

    # 플레이어 선택지 입력
    player_choice = input("Player: ")

    if (player_choice == "종료"):
        break

    # 선택지 메시지에 저장
    query = player_choice
    messages.append(
        {"role": "user", "content": query}
    )
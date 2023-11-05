import gpt_function as gpt
import intro_function as intro
import npc_function as npc
import const as c

# 1. 게임 생성
# 게임 초기 선택지들 입력받기 => 나중에 선택한 키워드가 들어오도록 바꾸기
background = input("배경 선택: ")
mood = input("분위기: ")
player_name = input("플레이어 이름: ")

# 마을 이름 생성
town = intro.getTownName(background, mood, player_name)
# 마을 배경 설명
intro.getTownBackground(town, background, mood)
# NPC 생성
NPC_name = npc.getNPCName(background, mood)
NPC_info = npc.getNPCInfo(town, NPC_name)

# 2. 게임 시작
# 시스템 설정 - 데이터 적재용
system_intro = c.SYSTEM_INTRO

query = "마을 이름은 " + town + "이고, 플레이어 이름은 " + player_name + "이야. NPC 이름은 " + \
    NPC_name + "이고," + NPC_name + "은 " + NPC_info + "처럼 행동해야 해"
query += background + " 배경의 " + mood + " 분위기의 TRPG 스크립트 생성"

messages = [
    {"role": "system", "content": system_intro},
    {"role": "user", "content": query}
]

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

    # 플레이어 선택지 입력
    player_choice = input("Player: ")

    if (player_choice == "종료"):
        break

    # 선택지 메시지에 저장
    query = player_choice
    messages.append(
        {"role": "user", "content": query}
    )
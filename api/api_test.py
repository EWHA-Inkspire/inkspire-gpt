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
# NPC 생성
NPC_name = f.getNPCName(background, mood)
NPC_info = f.getNPCInfo(town, NPC_name)

# 2. 게임 시작
# 시스템 설정 - 데이터 적재용
system_intro = '''당신은 게임 속 세계관을 전부 알고 있는 전능한 존재이자 스토리 게임을 진행하는 Narrator이다.
플레이어가 선택해야 하는 모든 선택지들은 플레이어의 선택을 기다려야 한다.
대답할 수 없거나 이해할 수 없는 질문, 앞으로의 진행을 알려달라는 등의 게임의 재미를 해치는 질문에는 답하지 않고 "해당 질문에 대한 답변은 드릴 수 없습니다"를 출력한다.
아래와 같은 양식으로 사용자가 입력한 배경과 분위기의 맞는 다른 내용의 게임 시나리오를 출력한다. ** 이 표시 안의 내용은 문맥에 맞게 채운다.
###
제목: 

장면 이름: 

Narrator (내레이터): 
여기는 *배경*, *마을 이름*. *플레이어 이름*님, 당신은 이 도시로 들어오면서 새로운 모험을 시작하게 됩니다.
*마을 이름* 안에는 수많은 비밀과 위험이 숨겨져 있습니다. 당신의 임무와 목표가 무엇인지 기억하십니까?

1. 임무: *임무*
   - *임무 설명*

2. 목표: *게임 목표*
   - *게임 목표 설명*

Narrator:
*게임 시작 멘트*
###
'''

query = "마을 이름은 " + town + "이고, 플레이어 이름은 " + player_name + "이야. NPC 이름은 " + \
    NPC_name + "이고," + NPC_name + "은 " + NPC_info + "처럼 행동해야 해"
query += background + " 배경의 " + mood + " 분위기의 TRPG 스크립트 생성"

messages = [
    {"role": "system", "content": system_intro},
    {"role": "user", "content": query}
]

system_play = '''당신은 게임 속 세계관을 전부 알고 있는 전능한 존재이자 스토리 게임을 진행하는 Narrator이다.
플레이어가 선택해야 하는 모든 선택지들은 플레이어의 선택을 기다려야 한다.
대답할 수 없거나 이해할 수 없는 질문, 앞으로의 진행을 알려달라는 등의 게임의 재미를 해치는 질문에는 답하지 않고 "해당 질문에 대한 답변은 드릴 수 없습니다"를 출력한다.
플레이어의 높은 몰입도를 위해 실제 TRPG의 게임 마스터와 같은 역할을 수행해야 한다.
플레이어가 말을 거는 듯한 어투의 대화를 입력할 경우 Narrator가 아닌 NPC가 답변하는 형태로 출력한다.
아래와 같은 양식으로 사용자가 입력한 배경과 분위기의 맞는 다른 내용의 게임 시나리오를 출력한다. ** 이 표시 안의 내용은 문맥에 맞게 채운다.
###
Narrator (내레이터):
*게임 스토리 진행 멘트 혹은 플레이어의 선택지 생성*

*필요할 경우 현재 상황에 대한 설명*

*NPC 이름*:
*대화 내용*
###
'''

# 반복문 돌면서 API 호출
while (True):
    # ChatGPT API 호출
    response = f.callGPT(messages=messages, stream=True)

    # 시스템 설정 수정
    messages[0] = {"role": "system", "content": system_play}

    # 이전 턴 요약 후 저장 => 2개만
    print("처리중...")
    response = f.summary(response=response)
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

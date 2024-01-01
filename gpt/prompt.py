from .gpt_function import *
from .intro_function import *
from .npc_function import *
from .objective_function import *
from .event_function import *
import gpt.const as c

# 1. 게임 생성
# 게임 초기 선택지들 입력받기 => 나중에 선택한 키워드가 들어오도록 바꾸기
background = input("배경 선택: ")
genre = input("장르: ")
player_name = input("플레이어 이름: ")

# 마을 이름 생성
town = getTownName(background, genre)
# 마을 배경 설명
town_detail = getTownBackground(town, background, genre)
# 조력자 NPC 생성
PNPC_name = getProtaNPCName(background, genre)
print("gpt done>> Pnpc")
PNPC_info = getProtaNPCInfo(town, PNPC_name)
print("gpt done>> Pnpc:desc")
#적대자 NPC 생성
ANPC_name = getAntaNPCName(background, genre)
print("gpt done>> Anpc")
ANPC_info = getAntaNPCInfo(town, ANPC_name)
print("gpt done>> Anpc:desc")
# 게임 목표 설정
final_title, final_content, final_req = setFinalObjective(town=town, town_detail=town_detail,genre=genre,background=background)

# 챕터 1 생성
chapter_num = 1
chapter_type, chapter_title, chapter_content, chapter_req, chapter_etc = setChapterObjective(chapter_num, [], final_title, final_content,town, town_detail, genre, background)

# 주사위 이벤트 등장 조건 생성
event_require, event_content, event_success, event_fail = setDiceEvent(town, genre, background, town_detail, chapter_content, chapter_req)

# 2. 게임 시작
# 시스템 설정 - 데이터 적재용
system_intro = c.SYSTEM_INTRO

query = "마을 이름은 " + town + "이고, 플레이어 이름은 " + player_name + "이야. 조력자 NPC 이름은 " + \
    PNPC_name + "이고," + PNPC_info + "처럼 행동해야 해. 적대자 NPC 이름은 " + \
    ANPC_name + "이고," + ANPC_info + "처럼 행동해야 해"
query+= "이 챕터는 스토리 플롯 단계 중 "+c.story_plot_title[chapter_num]+"이며 이 단계에서는"+c.story_plot[c.story_plot_title[chapter_num]]
query+= "이 게임의 최종 목표는 " + final_title + final_content + "이고 현재 챕터의 목표는 " + chapter_title + chapter_content + "이야."
query += background + " 배경의 " + genre + " 분위기의 TRPG 스크립트 생성"

messages = [
    {"role": "system", "content": system_intro},
    {"role": "user", "content": query}
]


# 챕터 목표 달성 여부 체크
# system_objective_checker = '''당신은 입력된 스크립트 내용에서 주어진 게임의 목표 달성 여부를 확인하는 objective checker이다. 
# 출력은 오로지 "True" 혹은 "False" 로만 한다. 
# 현재 플레이어의 목표는 '''+game_objective[curr_objective]+'''이고 목표에 대한 설명은 다음과 같다.
# '''+game_objective_summary[curr_objective]

system_play = c.SYSTEM_PLAY

# 반복문 돌면서 API 호출
while (True):
    # ChatGPT API 호출
    response = callGPT(messages=messages, stream=True)

    # 시스템 설정 수정
    messages[0] = {"role": "system", "content": system_play}

    # 이전 턴 요약 후 저장 => 2개만
    print(">> Call GPT: summarizing play data")
    response = summary(response=response)
    messages.append(
        {"role": "assistant", "content": response}
    )
    obj_check = checkObjective(chapter_title,chapter_content,chapter_req,response)
    if obj_check:
        chapter_num += 1
        chapter_type, chapter_title, chapter_content, chapter_req, chapter_etc = setChapterObjective(chapter_num, [], final_title, final_content,town, town_detail, genre, background)
    # 목표 달성 여부 체크
    # messages_objective = [
    #     {"role": "system", "content": system_objective_checker},
    # ]
    
    # messages_objective.append(messages[len(messages)-1])
        
    # print("현재 목표:"+str(curr_objective)+"\n"+game_objective[curr_objective]+"\n목표 달성 여부:")
    # response = gpt.callGPT(messages=messages_objective,stream=True)

    # if(response == "True"):
    #     if(curr_objective<len(game_objective)-1):
    #         curr_objective+=1
    #     elif(curr_objective==0):
    #         print("게임 종료")
    #     elif(curr_objective==4):
    #         curr_objective = 0

    # 플레이어 선택지 입력
    player_choice = input("Player: ")

    if (player_choice == "종료"):
        break

    # 선택지 메시지에 저장
    query = player_choice
    messages.append(
        {"role": "user", "content": query}
    )
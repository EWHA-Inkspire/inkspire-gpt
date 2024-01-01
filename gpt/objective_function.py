from gpt_function import callGPT
import const as c
import json

# 게임 최종 목표 설정 함수
def setFinalObjective(town,town_detail,genre,background):
    c.setVarSYSTEM_FINOBJ(town_detail,background)
    query = town+"이라는 이름의 마을에서 진행되는 게임의 "+ genre +"장르에 어울리는 게임 목표 생성"

    messages = [
        {"role": "system", "content": c.SYSTEM_FINOBJ},
        {"role": "user", "content": query}
    ]
    
    print(">> Call GPT: game objective")
    response = callGPT(messages=messages, stream=True)
    print(">> GPT Done: game objective")

    # 문자열 분리 기준자-> ":"
    response = response.replace('\n\n',':').replace('\n',':')
    response_arr = response.split(':')
    # 문자열 앞뒤 공백 삭제
    for k in response_arr:
        k = k.strip()

    final_title = response_arr[1]
    final_content = response_arr[3]
    final_req = response_arr[5]

    return final_title, final_content, final_req


# 챕터 목표 설정 함수
def setChapterObjective(chapter_num, prev_summary, final_title, final_content, town, town_detail, genre, background):
    c.setVarSYSTEM_CHAPTER(chapter_num, prev_summary, final_title, final_content, town_detail, background)
    query = town+"이라는 이름의 마을에서 진행되는 게임의 "+ genre +"장르에 어울리는 챕터 목표 생성"

    messages = [
        {"role": "system", "content": c.SYSTEM_CHAPTER},
        {"role": "user", "content": query}
    ]
    
    print(">> Call GPT: chapter objective")
    response = callGPT(messages=messages, stream=True)
    print(">> GPT Done: chapter objective")

    # 문자열 분리 기준자-> ":"
    response = response.replace('\n\n',':').replace('\n',':')
    response_arr = response.split(':')
    # 문자열 앞뒤 공백 삭제
    for k in response_arr:
        k = k.strip()

    chapter_type = int(response_arr[1])
    chapter_title = response_arr[3]
    chapter_content = response_arr[5]
    chapter_req = response_arr[7]
    chapter_etc = response_arr[9]


    '''챕터목표유형: *챕터 목표 유형을 숫자만 표시*
    챕터목표: *챕터 목표*
    챕터목표 설명: *챕터 목표 설명*
    달성 조건: *구체적인 달성 조건 아이템 습득이 목표일 때, 구체적인 아이템 이름이 포함된다.* 
    비고: *챕터 유형에 맞는 비고 생성*'''

    return chapter_type, chapter_title, chapter_content,chapter_req, chapter_etc


# 목표 달성 함수
def checkObjective(chapter_title, chapter_content, chapter_req, turn_summary):
    query = "현재 챕터 목표: "+chapter_title+"\n목표 설명: "+chapter_content+"\n달성 조건: "+chapter_req
    messages = [
        {"role": "system", "content": c.SYSTEM_OBJECTIVE_CHECKER},
        {"role": "user", "content": query}
    ]
    print(">> Call GPT: objective checker")
    response = callGPT(messages=messages, stream=True)
    print(">> GPT Done: objective checker")

    if response == "True":
        return True
    elif response == "False":
        return False
    print(">> ERROR obective checker: Wrong Return Format")
    return False


# Json 파싱함수
def objectiveToJson(objective, summary):
    json_dic = {
        "final_obj": objective[0],
        "final_summary": summary[0],
        "minor_obj": [],
        "minor_summary": []
    }

    for i in range(1,len(objective)):
        json_dic["minor_obj"].append(objective[i]) 
        json_dic["minor_summary"].append(summary[i]) 
    

    with open("objective_data.json","w",encoding='utf-8') as file:
        json.dump(json_dic,file,indent='\t',ensure_ascii=False)

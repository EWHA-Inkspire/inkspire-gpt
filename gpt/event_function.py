from gpt_function import callGPT
import const as c

# 이벤트 내용 및 발생 조건 생성 함수
def setEventInfo(town, genre, background, town_detail, obj, obj_require):
    c.setVarSYSTEM_EVENT(obj, obj_require, background, town_detail)
    query = town+"이라는 이름의 마을에서 진행되는 게임의 "+ genre +" 장르에 어울리는 주사위 이벤트 내용 생성"
    
    messages = [
        {"role": "system", "content": c.SYSTEM_EVENT},
        {"role": "user", "content": query}
    ]
    
    print(">> Call GPT: create event")
    response = callGPT(messages=messages, stream=True)
    print(">> GPT Done: create event")
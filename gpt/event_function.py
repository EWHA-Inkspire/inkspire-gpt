from .gpt_function import callGPT
import gpt.const as c

# 이벤트 내용 및 발생 조건 생성 함수
def setDiceEvent(background, town_detail, obj, obj_require):
    SYSTEM = c.setVarSYSTEM_EVENT(obj, obj_require, background, town_detail)
    query = "챕터 목표와 관련있는 주사위 이벤트 발생 조건 생성"
    
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": query}
    ]
    
    print(">> Call GPT: create event")
    response = callGPT(messages=messages, stream=True)
    print(">> GPT Done: create event")
    
    # 문자열 분리 기준자-> ":"
    response = response.replace('\n\n','\n').replace('\n', ':')
    response_arr = response.split(':')
    for k in response_arr:
        k = k.strip()
    
    event_require = response_arr[1]
    event_content = response_arr[3]
    event_success = response_arr[5]
    event_fail = response_arr[7]
    
    return event_require, event_content, event_success, event_fail

# 이벤트 발생 여부 체크 => 이벤트 발생 조건, 내용, player의 입력값에 대한 gpt response 필요
def checkEvent(event_req, event_content, query):
    SYSTEM = c.setVarSYSTEM_EVENT_CHECKER(event_req, event_content)
    
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": query}
    ]
    
    print("callGPT")
    response = callGPT(messages=messages, stream=True)
    
    # 문자열 분리 기준자-> ":"
    response = response.replace('Checker:','')
    response = response.strip()
    print(response)
    return response

# event_req = "플레이어가 숲으로 향해 천둥 망치를 찾으러 이동했을 때"
# event_content = "숲 속에서 이상한 소리가 들린다. 플레이어는 무엇인가 특별한 것을 발견하기 위해 조사하려 한다."

# query = '''Narrator (내레이터):
# 청록마을 주변의 숲은 밀림과 같은 조용한 공간으로 알려져 있습니다. 이곳은 마을 주민들에게는 휴식과 여유를 제공하는 장소로 여겨지고 있으며, 다양한 식물과 동물들이 서식하고 있습니다. 그러나 최근 몇 주 동안 몹시 세게가 늘어난 탓에, 숲의 길은 잠시 닫힌 상태입니다. 소민님은 숲을 통해 이동하기 위해서는 다른 길을 찾아야 할 것입니다.

# 이제 어떤 선택을 하시겠습니까?

# 1. 예리에게 도움을 청하고 다른 길을 찾아본다.
# 2. 청록마을 주변을 탐색하여 다른 입구를 찾아본다.
# 3. 신옥에게 도움을 청하고 길을 찾아본다.
# 4. 기다리며 다른 사람들의 이야기를 들어본다.
# Player: 4. 기다리며 다른 사람들의 이야기를 들어본다.
# '''

# checkEvent(event_req, event_content, query)
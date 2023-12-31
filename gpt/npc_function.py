from .gpt_function import callGPT

# 조력자 이름 생성
def getProtaNPCName(background, genre):
    npc_setting = "너는 조력자 NPC 캐릭터의 이름을 한 단어로 출력해야 해."
    query = background + " 배경의 " + genre + "분위기에 어울리는 조력자 NPC 이름 1개를 출력해줘"

    messages = [
        {"role": "system", "content": npc_setting},
        {"role": "user", "content": query}
    ]

    PNPC_name = callGPT(messages=messages, stream=False)

    return PNPC_name

# 조력자 설정 생성
def getProtaNPCInfo(town, PNPC_name):
    npc_setting = "조력자 NPC는 " + town + \
        "에 어울리는 직업을 가져야 하고, 성격에 맞게 존댓말 혹은 반말 중 하나의 말투만을 일관되게 사용해야 해."
    query = town + "의 조력자 NPC인" + PNPC_name + "의 직업, 그리고 성격과 말투를 설명해줘."

    messages = [
        {"role": "system", "content": npc_setting},
        {"role": "user", "content": query}
    ]

    PNPC_info = callGPT(messages=messages, stream=False)

    return PNPC_info

# 적대자 NPC 이름 생성
def getAntaNPCName(background, genre):
    npc_setting = "너는 적대자 NPC 캐릭터의 이름을 한 단어로 출력해야 해."
    query = background + " 배경의 " + genre + "분위기에 어울리는 적대자 NPC 이름 1개를 출력해줘"

    messages = [
        {"role": "system", "content": npc_setting},
        {"role": "user", "content": query}
    ]

    ANPC_name = callGPT(messages=messages, stream=False)

    return ANPC_name

# 적대자 NPC 설정 생성
def getAntaNPCInfo(town, ANPC_name):
    npc_setting = "적대자 NPC는 " + town + \
        "에 어울리는 직업을 가져야 하고, 성격에 맞게 존댓말 혹은 반말 중 하나의 말투만을 일관되게 사용해야 해."
    query = town + "의 적대자 NPC인" + ANPC_name + "의 직업, 그리고 성격과 말투를 설명해줘."

    messages = [
        {"role": "system", "content": npc_setting},
        {"role": "user", "content": query}
    ]

    ANPC_info = callGPT(messages=messages, stream=False)

    return ANPC_info
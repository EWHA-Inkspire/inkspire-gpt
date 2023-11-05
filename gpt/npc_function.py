from gpt_function import callGPT

# NPC 이름 생성
def getNPCName(background, mood):
    npc_setting = "너는 NPC 캐릭터의 이름을 한 단어로 출력해야 해."
    query = background + " 배경의 " + mood + "분위기에 어울리는 NPC 이름 1개를 출력해줘"

    messages = [
        {"role": "system", "content": npc_setting},
        {"role": "user", "content": query}
    ]

    response = callGPT(messages=messages, stream=False)

    NPC_name = response['choices'][0]['message']['content']

    return NPC_name

# NPC 설정 생성
def getNPCInfo(town, NPC_name):
    npc_setting = "NPC는 " + town + \
        "에 어울리는 직업을 가져야 하고, 성격에 맞게 존댓말 혹은 반말 중 하나의 말투만을 일관되게 사용해야 해."
    query = town + "의 NPC인" + NPC_name + "의 직업, 그리고 성격과 말투를 설명해줘."

    messages = [
        {"role": "system", "content": npc_setting},
        {"role": "user", "content": query}
    ]

    response = callGPT(messages=messages, stream=False)

    NPC_info = response['choices'][0]['message']['content']

    return NPC_info
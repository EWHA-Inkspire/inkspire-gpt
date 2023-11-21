from .gpt_function import callGPT

# 배경, 분위기에 맞는 마을 이름 생성
def getTownName(background, genre):
    # 마을 이름 출력을 위한 세팅 & 쿼리
    town_setting = "너는 항상 한 단어로만 답을 출력해야해"
    query = background + " 배경의 " + genre + "분위기에 어울리는 마을 이름 1개를 출력해줘"

    messages = [
        {"role": "system", "content": town_setting},
        {"role": "user", "content": query}
    ]

    town = callGPT(messages=messages, stream=False)

    return town

# 배경에 대한 설명
def getTownBackground(town, background, genre):
    town_setting = "사용자가 시나리오 속 캐릭터라고 상정하고 " + background + \
        " 배경과 " + genre + " 분위기에 어울리는 마을 이름을 사용자가 입력하면 그 배경에 대해 설명해 줘."
    query = town + "의 배경에 대해 자세히 설명해줘"

    messages = [
        {"role": "system", "content": town_setting},
        {"role": "user", "content": query}
    ]

    town_detail = callGPT(messages=messages, stream=False)
    return town_detail

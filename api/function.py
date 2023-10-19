import openai
import os

# 환경변수로 설정해 둔 API 키 받아오기
openai.api_key = os.getenv("OPENAI_API_KEY")

# GPT 출력값 스트림 형태로 출력 & 결과값 반환


def printStream(response):
    answer = ""
    # Print the ChatGPT response within a loop.
    for chunk in response:
        print(
            chunk.choices[0].delta.get("content", ""),
            end=""  # This will put all the streamed chunks on one line.
        )
        answer += chunk.choices[0].delta.get("content", "")
    print("\n")

    return answer

# GPT API 호출 함수 & 스트림 형태 출력


def callGPT(messages, stream):
    model = "gpt-3.5-turbo"

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        stream=stream,
        temperature=0,  # 랜덤성 조절
    )

    if (stream):
        return printStream(response=response)

    return response

# 배경, 분위기에 맞는 마을 이름 생성


def getTownName(background, mood, player_name):
    # 마을 이름 출력을 위한 세팅 & 쿼리
    town_setting = "너는 항상 한 단어로만 답을 출력해야해"
    query = background + " 배경의 " + mood + "분위기에 어울리는 마을 이름 1개를 출력해줘"

    messages = [
        {"role": "system", "content": town_setting},
        {"role": "user", "content": query}
    ]

    response = callGPT(messages=messages, stream=False)

    town = response['choices'][0]['message']['content']
    print("안녕하세요 " + player_name + "님. 지금부터 당신을 " + town + "에 초대합니다.\n")

    return town

# 배경에 대한 설명


def getTownBackground(town, background, mood):
    town_setting = "사용자가 시나리오 속 캐릭터라고 상정하고 " + background + \
        " 배경의 " + mood + " 분위기의 TRPG 시나리오를 진행해줘."
    query = town + "의 배경에 대해 자세히 설명해줘"

    messages = [
        {"role": "system", "content": town_setting},
        {"role": "user", "content": query}
    ]

    callGPT(messages=messages, stream=True)

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

# 응답 요약


def summary(response):
    query = response + " 요약"
    messages = [
        {"role": "user", "content": query}
    ]

    response = callGPT(messages=messages, stream=False)

    return response['choices'][0]['message']['content']

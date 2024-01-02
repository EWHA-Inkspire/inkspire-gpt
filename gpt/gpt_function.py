import openai
from dotenv import load_dotenv
import os

load_dotenv()

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
        temperature=0.7,  # 랜덤성 조절
    )

    if (stream):
        return printStream(response=response)

    return response['choices'][0]['message']['content']

# 응답 요약
def summary(response):
    query = response + " 중요 내용 요약해 줘"
    messages = [
        {"role": "system", "content": "너는 문장들이 들어오면 그것을 중요한 내용 위주로 요약한 것만을 답해야 해."},
        {"role": "user", "content": query}
    ]

    response = callGPT(messages=messages, stream=False)

    return response

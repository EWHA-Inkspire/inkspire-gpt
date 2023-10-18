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
            end = "" # This will put all the streamed chunks on one line.
        )
        answer += chunk.choices[0].delta.get("content", "")
    print("\n")

    return answer
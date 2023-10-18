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

# GPT API 호출 함수 & 스트림 형태 출력
def callGPT(messages, stream): 
    model = "gpt-3.5-turbo"
    
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        stream = stream,
        temperature = 0, # 랜덤성 조절
    )
    
    if(stream):
        return printStream(response=response)
    
    return response
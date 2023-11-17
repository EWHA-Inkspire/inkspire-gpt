import gpt_function as gpt
import json

# 게임 목표 설정
def setGameObjective(town,town_detail,genre,background):
    objective_setting = '''당신은 진행될 게임의 최종 목표와 최종목표를 이루기 위한 세부목표를 제시한다.
    세 가지의 세부 목표를 순서대로 모두 달성하면 자연스럽게 최종 목표에 도달할 수 있도록 설정한다. 

    다음은 게임의 배경인 
    '''+background+"배경의 마을에 대한 설명이다."+town_detail+'''
    아래와 같은 양식으로 게임의 목표를 설정한다. ** 이 표시 안의 내용은 문맥에 맞게 채운다.
    

    최종목표: *최종 목표*
    최종목표 설명: *최종 목표 설명*

    세부 목표1:*세부 목표1*
    설명: *세부 목표 1 설명*

    세부 목표2:*세부 목표2*
    설명: *세부 목표 2 설명*

    세부 목표3:*세부 목표3*
    설명: *세부 목표 3 설명*
    
    '''

    query = town+"이라는 이름의 마을에서 진행되는 게임의 "+genre +"장르에 어울리는 게임 목표 생성"

    messages = [
        {"role": "system", "content": objective_setting},
        {"role": "user", "content": query}
    ]
    
    print(">> Call GPT: game objective")
    response = gpt.callGPT(messages=messages, stream=True)
    print(">> GPT Done: game objective")

    response = response.replace('\n\n',':').replace('\n',':')
    response_arr = response.split(':')
    for k in response_arr:
        k = k.strip()
    
    objective = []
    summary = []
    
    for j in range(0,len(response_arr),4):
        objective.append(response_arr[j+1])
        summary.append(response_arr[j+3])

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
    return objective, summary

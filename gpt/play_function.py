from scenario.models import Npc, Goal
import gpt.const as c

def setTown(town, town_detail, player_name):

    query = "마을 이름은 #" + town + "#이고, 마을 배경 설명은 #" + town_detail + "#이다. 플레이어 이름은 #" + player_name + "#이다. "
    return query

def setBackground(background, genre):
    query = "#" + background + "# 배경의 #" + genre + "# 분위기의 TRPG 스크립트 생성"
    
    return query

def setNpc(npcs):
    for npc in npcs:
        if npc.role == 'anta':
            ANPC_info = npc.info
        elif npc.role == 'prota':
            PNPC_info = npc.info
            
    query =  "조력자 NPC는 #" + PNPC_info + "#처럼 행동해야 한다. 적대자 NPC는 #" + ANPC_info + "#처럼 행동해야 한다. "
    return query

def setPlot(chapter_num):
    query = "이 챕터는 스토리 플롯 단계 중 #"+c.story_plot_title[chapter_num]+"#이며 이 단계에서는 #"+c.story_plot[c.story_plot_title[chapter_num]] + "# "
    
    return query

def setGoal(c_goal, chapter):
    title = content = require = ""

    if c_goal.exists():
        goal = c_goal.first()
        title = goal.title
        content = goal.content
        require = goal.require
        
    if chapter == 5:
        query = "현재 챕터는 게임의 마지막 단계이다. 현재 챕터의 목표는 #" + title + " " + content + "#이다. 최종 목표 달성 조건은 #" + require + "#이다. " 
    else:
        query = "현재 챕터의 목표는 #" + title + " " + content + "#이다. 챕터 목표 달성 조건은 #" + require + "#이다. "
    
    return query

def setIntroQuery(request):
    
    town = request.data.get('town')
    town_detail = request.data.get('town_detail')
    player_name = request.data.get('player_name')
    query = setTown(town, town_detail, player_name)
    
    background = request.data.get('background')
    genre = request.data.get('genre')
    query += setBackground(background, genre)
    
    return query

def setPlayQuery(request):
    script_id = request.data.get('script_id')
    
    npcs = Npc.objects.filter(script_id=script_id)
    player_name = request.data.get('player_name')
    query = "플레이어 이름은 #" + player_name + "#이다. "
    query += setNpc(npcs)
    
    chapter = request.data.get('chapter')
    goal = Goal.objects.filter(script_id=script_id).filter(chapter=chapter)
    query += setGoal(goal, chapter)
    
    if(chapter != 0):
        chapter -= 1
    query += setPlot(chapter)
    
    return query
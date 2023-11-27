from scenario.models import Npc, Goal
import gpt.const as c

def setTown(town, player_name, npcs):
    for npc in npcs:
        if npc.role == 'anta':
            ANPC_info = npc.info
        elif npc.role == 'prota':
            PNPC_info = npc.info

    query = "마을 이름은 #" + town + "#이고, 플레이어 이름은 #" + player_name + "#이야. 조력자 NPC는 #" + \
    PNPC_info + "#처럼 행동해야 해. 적대자 NPC는 #" + ANPC_info + "#처럼 행동해야 해"

    return query

def setPlot(chapter_num):
    query = "이 챕터는 스토리 플롯 단계 중 #"+c.story_plot_title[chapter_num]+"#이며 이 단계에서는 #"+c.story_plot[c.story_plot_title[chapter_num]] + "#"
    
    return query

def setGoal(f_goal, c_goal):
    final_title = final_content = chapter_title = chapter_content = ""

    if f_goal.exists():
        final_goal = f_goal.first()
        final_title = final_goal.title
        final_content = final_goal.content

    if c_goal.exists():
        chapter_goal = c_goal.first()
        chapter_title = chapter_goal.title
        chapter_content = chapter_goal.content
    
    query = "이 게임의 최종 목표는 #" + final_title + final_content + "#이고 현재 챕터의 목표는 #" + chapter_title + chapter_content + "#이야."
    
    return query

def setBackground(background, genre):
    query = "#" + background + "# 배경의 #" + genre + "# 분위기의 TRPG 스크립트 생성"
    
    return query

def setIntroQuery(request):
    script_id = request.data.get('script_id')
    
    town = request.data.get('town')
    player_name = request.data.get('player_name')
    npcs = Npc.objects.filter(script_id=script_id)
    query = setTown(town, player_name, npcs)
    
    chapter = request.data.get('chapter')
    query += setPlot(chapter)
    
    f_goal = Goal.objects.filter(script_id=script_id).filter(chapter=5)
    c_goal = Goal.objects.filter(script_id=script_id).filter(chapter=chapter)
    query += setGoal(f_goal, c_goal)
    
    background = request.data.get('background')
    genre = request.data.get('genre')
    query += setBackground(background, genre)
    
    return query
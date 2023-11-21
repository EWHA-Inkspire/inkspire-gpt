from .models import *
from rest_framework import serializers

# 스크립트 정보 - 캐릭터와 맵핑되는 정보 (목표, gpt 제외)
class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ['script_id', 'background', 'genre', 'town', 'town_detail']

# 목표 정보
class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['goal_id', 'chapter', 'title', 'content', 'require', 'req_type', 'etc', 'finished']

# GPT 정보
class GptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gpt
        fields = ['gpt_id', 'chapter', 'role', 'query']

# npc 정보 - 이름, 역할, 직업, 말투, 성격
class NpcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Npc
        fields = ['name', 'role', 'info']

# 스크립트 세부 정보 - 스크립트 내용, 목표
class ScriptDetailSerializer(serializers.ModelSerializer):
    # 스크립트가 지닌 목표 정보
    goals = GoalSerializer(many=True, read_only=True)
    # 스크립트가 지닌 npc 정보
    npcs = NpcSerializer(many=True, read_only=True)
    
    class Meta:
        model = Script
        fields = ['background', 'genre', 'town', 'town_detail', 'goals', 'npcs']
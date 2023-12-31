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
        fields = ['goal_id', 'chapter', 'title', 'content', 'require', 'type', 'etc', 'finished']

# 이벤트 정보
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['goal_id', 'content', 'require', 'event_req', 'event_content', 'success', 'fail']

# GPT 정보
class GptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gpt
        fields = ['gpt_id', 'chapter', 'role', 'content', 'summary']

# npc 정보 - 이름, 역할, 정보
class NpcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Npc
        fields = ['name', 'role', 'info']

# 훈련 데이터 세트 정보 - 역할, 내용
class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ['role', 'content']

# 스크립트 세부 정보 - 스크립트 내용, 목표
class ScriptDetailSerializer(serializers.ModelSerializer):
    # 스크립트가 지닌 목표 정보
    goals = GoalSerializer(many=True, read_only=True)
    # 스크립트가 지닌 npc 정보
    npcs = NpcSerializer(many=True, read_only=True)
    
    class Meta:
        model = Script
        fields = ['background', 'genre', 'town', 'town_detail', 'goals', 'npcs']
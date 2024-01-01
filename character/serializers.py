from .models import *
from scenario.serializers import ScriptSerializer
from rest_framework import serializers

# 캐릭터 정보
class CharacterSerializer(serializers.ModelSerializer):
    # 캐릭터가 지닌 스크립트 정보
    script = ScriptSerializer(many=False, read_only=True)
    class Meta:
        model = Character
        fields = ['character_id', 'name', 'attack', 'defense', 'hp', 'agility', 'intelligence', 'script']
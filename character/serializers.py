from .models import *
from scenario.serializers import ScriptSerializer
from rest_framework import serializers

# 인벤토리 정보
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['item_id', 'name', 'type', 'detail']
        
# 캐릭터 정보
class CharacterSerializer(serializers.ModelSerializer):
    # 캐릭터가 지닌 스크립트 정보
    script = ScriptSerializer(many=False, read_only=True)
    # 캐릭터가 지닌 인벤토리 정보
    inventory = InventorySerializer(many=False, read_only=True)
    class Meta:
        model = Character
        fields = ['character_id', 'name', 'inventory', 'attack', 'defense', 'hp', 'agility', 'intelligence', 'script']

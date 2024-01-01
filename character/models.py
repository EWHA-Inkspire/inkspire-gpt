from django.db import models
from account.models import User

# 캐릭터 모델
class Character(models.Model):
    # character_id : 자동 생성 (PK)
    character_id = models.AutoField(primary_key=True)
    
    # 외래키 지정 (User - Character -> 1 : N 관계)
    user = models.ForeignKey(User, related_name="characters", on_delete=models.CASCADE, db_column="user_id")
    
    # 캐릭터 이름
    name = models.CharField(default='', max_length=100, null=False, blank=False)
    # 캐릭터 스탯 : 공격력, 방어력, 체력, 민첩성, 지능
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    hp = models.IntegerField(default=0)
    agility = models.IntegerField(default=0)
    intelligence = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

# 인벤토리 모델
class Inventory(models.Model):
    # item_id : 자동 생성 (PK)
    item_id = models.AutoField(primary_key=True)
    
    # 외래키 지정 (Character - Inventory -> 1 : N 관계)
    character = models.ForeignKey(Character, related_name="inventory", on_delete=models.CASCADE, db_column="character_id")
    
    # 아이템 명
    name = models.CharField(default='', max_length=50, null=False, blank=False)
    # 아이템 유형
    type = models.CharField(max_length=10, null=False, blank=False)
    # 아이템 설명
    detail = models.CharField(default='', max_length=300, null=True, blank=True)
    # 수량
    num = models.IntegerField(default=1)
    
    def __str__(self):
        return self.name
from django.db import models
from account.models import Character

# 스크립트 모델
class Script(models.Model):
    # script_id : 자동 생성 (PK)
    script_id = models.BigAutoField(primary_key=True)
    
    # 외래키 지정 (Character - Script -> 1 : 1 관계)
    character = models.OneToOneField(Character, related_name="script", on_delete=models.CASCADE, db_column="character_id")
    
    # 스크립트 배경
    background = models.CharField(default='', max_length=100, null=False, blank=False)
    # 스크립트 장르
    genre = models.CharField(default='', max_length=50, null=False, blank=False)
    # 마을 이름
    town = models.CharField(default='', max_length=50, null=True)
    # 마을 설명
    town_detail = models.TextField(default='', null=True)
    
    def __str__(self):
        return self.background + ", " + self.genre + ": " + self.town

# 목표 모델
class Goal(models.Model):
    # goal_id : 자동 생성 (PK)
    goal_id = models.BigAutoField(primary_key=True)
    
    # 외래키 지정 (Script - Goal -> 1 : N 관계)
    script = models.ForeignKey(Script, related_name="goals", on_delete=models.CASCADE, db_column="script_id")
    
    # 최종 목표 여부
    final = models.BooleanField(default=False)
    # 목표 내용
    content = models.TextField(default='', null=False, blank=False)
    # 목표 달성 여부
    finished = models.BooleanField(default=False)
    
    def __str__(self):
        return self.content

# GPT 모델
class Gpt(models.Model):
    # gpt_id : 자동 생성 (PK)
    gpt_id = models.BigAutoField(primary_key=True)
    
    # 외래키 지정 (Script - Gpt -> 1 : N 관계)
    script = models.ForeignKey(Script, related_name='gpts', on_delete=models.CASCADE, db_column="script_id")
    
    # 역할
    role = models.CharField(default='', max_length=10, null=False, blank=False)
    # 쿼리
    query = models.TextField(default='', null=True)
    
    def __str__(self):
        return self.query

# NPC 모델
class Npc(models.Model):
    ROLE_CHOICES = (
        ('prota', 'prota'),
        ('anta', 'anta'),
    )
    # npc_id : 자동 생성 (PK)
    npc_id = models.BigAutoField(primary_key=True)
    
    # 외래키 지정 (Script - Gpt -> 1 : N 관계)
    script = models.ForeignKey(Script, related_name='npcs', on_delete=models.CASCADE, db_column="script_id")
    
    # npc 이름
    name = models.CharField(default='', max_length=100, null=False, blank=False)
    # 역할
    role = models.CharField(default='', choices=ROLE_CHOICES, max_length=10, null=False, blank=False)
    # 직업
    job = models.CharField(default='', max_length=100, null=False, blank=False)
    
    def __str__(self):
        return self.name
    
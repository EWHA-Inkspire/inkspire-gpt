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
    
    # 속한 챕터 (총 5개의 챕터로 시나리오 구분)
    chapter = models.IntegerField(default=0)
    # 목표 제목
    title = models.TextField(default='', null=False, blank=False)
    # 목표 내용
    content = models.TextField(default='', null=False, blank=False)
    # 달성 조건
    require = models.TextField(default='', null=False, blank=False)
    # 달성 유형
    req_type = models.IntegerField(default=0)
    # 비고
    etc = models.TextField(default='', null=True, blank=True)
    
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
   
    # 속한 챕터 (총 5개의 챕터로 시나리오 구분)
    chapter = models.IntegerField(default=0)
    # 역할
    role = models.CharField(default='', max_length=10, null=False, blank=False)
    # 내용
    content = models.TextField(default='', null=True)
    # 요약
    summary = models.TextField(default='', null=False, blank=False)
    
    def __str__(self):
        return self.query

# NPC 모델
class Npc(models.Model):
    # npc_id : 자동 생성 (PK)
    npc_id = models.BigAutoField(primary_key=True)
    
    # 외래키 지정 (Script - Gpt -> 1 : N 관계)
    script = models.ForeignKey(Script, related_name='npcs', on_delete=models.CASCADE, db_column="script_id")
    
    # npc 이름
    name = models.CharField(default='', max_length=300, null=False, blank=False)
    # 역할 (prota or anta)
    role = models.CharField(default='', max_length=10, null=False, blank=False)
    # 정보
    info = models.TextField(default='',null=False, blank=False)
    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# 회원 모델
# AbstractBaseUser : id, password, last_login 필드
class User(AbstractBaseUser):
    # user_id : 자동 생성 (PK)
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(default='', max_length=254, null=False, blank=False, unique=True)
    nickname=models.CharField(default='', max_length=100, null=False, blank=False, unique=True)
    
    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    # 헬퍼 클래스 사용
    objects = BaseUserManager()
    
    # 사용자의 username field 닉네임으로 설정
    USERNAME_FIELD = 'nickname'
    
    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = ['email', 'password']
    
    def __str__(self):
        return self.nickname
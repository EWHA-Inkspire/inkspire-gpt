from django.urls import path, include
from .views import *

urlpatterns = [
    # 캐릭터 생성/조회
    path('character', CharacterView.as_view())
]
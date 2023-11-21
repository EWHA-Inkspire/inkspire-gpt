from django.shortcuts import get_object_or_404

from .models import *

# 권한 확인 함수
def CheckAuth(user, model_name, pk):
    model = get_object_or_404(model_name, pk=pk)
    
    if model_name == Character:
        return model.user != user
    else:
        return model.character.user != user
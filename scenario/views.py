from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication

from .models import *

# 권한 확인 함수
def CheckAuth(user, model_name, pk):
    model = get_object_or_404(model_name, pk=pk)
    
    if model_name == Character:
        return model.user != user
    else:
        return model.character.user != user
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication

from .views import *
from .models import *
from .serializers import *
from account.models import *
from account.views import get_token_key, get_user_id_from_token
from gpt.intro_function import *

# 스크립트 정보 저장 뷰 (pk : character_id)
class ScriptView(views.APIView):
    serializer_class = ScriptSerializer
    
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def post(self, request, pk):
        auth_token = get_token_key(request=request)
        user_id = get_user_id_from_token(token_key=auth_token)
        user = get_object_or_404(User, pk=user_id)
        
        if CheckAuth(user=user, model_name=Character, pk=pk):
            return Response({
                'message' : '스크립트 생성 권한이 없습니다.'
            }, status=HTTP_400_BAD_REQUEST)
        
        character = get_object_or_404(Character, pk=pk)    
        serializer = self.serializer_class(data=request.data)
            
        if serializer.is_valid(raise_exception=True):
            # 입력받은 배경 및 장르를 토대로 마을 이름 & 배경 생성
            background = serializer.validated_data.get('background')
            genre = serializer.validated_data.get('genre')
            
            town_name = getTownName(background=background, genre=genre)
            town_detail = getTownBackground(town=town_name, background=background, genre=genre)
            
            # 시리얼라이저에 정보 추가
            serializer.validated_data['town'] = town_name
            serializer.validated_data['town_detail'] = town_detail
            
            serializer.save(character=character)
            
            return Response({
                'message' : '스크립트 생성 성공',
                'data' : serializer.data
            }, status=HTTP_200_OK)
        else:
            return Response({
                'message' : '스크립트 생성 실패',
                'data' : serializer.errors
            }, status=HTTP_400_BAD_REQUEST)

# 스크립트 상세 조회 뷰 (pk : script_id)
class ScriptListView(views.APIView):
    serializer_class = ScriptDetailSerializer
    
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def get(self, request, pk):
        auth_token = get_token_key(request=request)
        user_id = get_user_id_from_token(token_key=auth_token)
        user = get_object_or_404(User, pk=user_id)
        
        if CheckAuth(user=user, model_name=Script, pk=pk):
            return Response({
                    'message' : '스크립트 조회 권한이 없습니다.'
                }, status=HTTP_400_BAD_REQUEST)
        
        script = get_object_or_404(Script, pk=pk)
        serializer = self.serializer_class(script)
        
        return Response({
            'message' : '스크립트 상세 조회 성공',
            'data' : serializer.data
        }, status=HTTP_200_OK)

from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication

from .models import *
from .serializers import *
from account.models import *
from account.views import get_token_key, get_user_id_from_token
from gpt.intro_function import *

# 권한 확인 함수
def CheckAuth(user, model_name, pk):
    model = get_object_or_404(model_name, pk=pk)
    
    if model_name == Character:
        return model.user != user
    else:
        return model.character.user != user

# 스크립트 정보 저장 뷰 (pk : character_id)
class ScriptView(views.APIView):
    serilalizer_class = ScriptSerializer
    
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
        serializer = self.serilalizer_class(data=request.data)
            
        if serializer.is_valid(raise_exception=True):
            # 입력받은 배경 및 장르를 토대로 마을 이름 & 배경 생성
            background = serializer.validated_data.get('background')
            genre = serializer.validated_data.get('genre')
            player_name = character.name
            
            town_name = getTownName(background=background, genre=genre, player_name=player_name)
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
    serilalizer_class = ScriptDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        if CheckAuth(request, Script, pk):
            return Response({
                    'message' : '스크립트 조회 권한이 없습니다.'
                }, status=HTTP_400_BAD_REQUEST)
        
        script = get_object_or_404(Script, pk=pk)
        serializer = self.serilalizer_class(script)
        
        return Response({
            'message' : '스크립트 상세 조회 성공',
            'data' : serializer.data
        }, status=HTTP_200_OK)

# 목표 리스트 뷰 (pk : script_id)
class GoalListView(views.APIView):
    serilalizer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        if CheckAuth(request, Script, pk):
            return Response({
                'message' : '목표 생성 권한이 없습니다.'
            })
        
        script = get_object_or_404(Script, pk=pk)
        serializer = self.serilalizer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(script=script)
            return Response({
                'message' : '목표 생성 성공',
                'data' : serializer.data
            }, status=HTTP_200_OK)
        else:
            return Response({
                'message' : '목표 생성 실패',
                'data' : serializer.errors
            }, status=HTTP_400_BAD_REQUEST)

# 목표 상세 뷰 (pk : script_id, goal_pk : goal_id)
class GoalDetailView(views.APIView):
    serilalizer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        goal = get_object_or_404(Goal, pk=pk)
        self.check_object_permissions(self.request, goal.script)
        return goal
    
    def get(self, request, pk, goal_pk):
        if CheckAuth(request, Script, pk):
            return Response({
                'message' : '목표 상세 조회 권한이 없습니다.'
            }, status=HTTP_400_BAD_REQUEST)
        
        goal = self.get_object(pk=goal_pk)
        serializer = self.serilalizer_class(goal)
        
        return Response({
            'message' : '목표 상세 조회 성공',
            'data' : serializer.data
        }, status=HTTP_200_OK)
    
    def patch(self, request, pk, goal_pk):
        if CheckAuth(request, Script, pk):
            return Response({
                'message' : '목표 정보 수정 권한이 없습니다.'
            }, status=HTTP_400_BAD_REQUEST)
        
        goal = self.get_object(pk=goal_pk)
        serializer = self.serilalizer_class(data=request.data, instance=goal, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message' : '목표 정보 수정 성공',
                'data' : serializer.data
            }, status=HTTP_200_OK)
        else:
            return Response({
                'message' : '목표 정보 수정 실패',
                'data' : serializer.errors
            }, status=HTTP_400_BAD_REQUEST)

# GPT 대화내용 (pk : script_id)
class GptView(views.APIView):
    serilalizer_class = GptSerializer
    
    def post(self, request, pk):
        script = get_object_or_404(Script, pk=pk)
        serializer = self.serilalizer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(script=script)
            return Response({
                'message' : 'GPT 쿼리 저장 성공',
                'data' : serializer.data
            }, status=HTTP_200_OK)
        else:
            return Response({
                'message' : 'GPT 쿼리 저장 실패',
                'data' : serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk):
        gpts = Gpt.objects.filter(script=pk)
        serializer = self.serilalizer_class(gpts, many=True)
        
        return Response({
            'message' : 'GPT 조회 성공',
            'data' : serializer.data
        }, status=HTTP_200_OK)
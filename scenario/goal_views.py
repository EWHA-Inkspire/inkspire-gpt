from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication

from .views import *
from .serializers import GoalSerializer
from account.models import User
from account.views import get_token_key, get_user_id_from_token
from gpt.intro_function import *
from gpt.objective_function import *

# 목표 생성 뷰 (pk : script_id, chapter: 1~5)
# script/<int:pk>/<int:chapter>/goal
# chapter가 0인 경우 목표 전체 조회
# chapter 1-5 : 해당 챕터 목표 조회
class GoalListView(views.APIView):
    serializer_class = GoalSerializer
    
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def post(self, request, pk, chapter):
        auth_token = get_token_key(request=request)
        user_id = get_user_id_from_token(token_key=auth_token)
        user = get_object_or_404(User, pk=user_id)
        
        if CheckAuth(user=user, model_name=Script, pk=pk):
            return Response({
                'message' : '목표 생성 권한이 없습니다.'
            })
        
        # 목표 생성에 필요한 정보 (town, town_detail, genre, background)
        script = get_object_or_404(Script, pk=pk)
        background = script.background
        genre = script.genre
        town = script.town
        town_detail = script.town_detail
        
        goals = []
        
        # chapter가 1일때는 최종 & 1챕터 목표 생성
        if chapter == 0:
            for i in range(0, 2):
                goal = {'chapter' : 0, 'title' : '', 'content': '', 'require' : '', 'req_type': 0, 'etc' : ''}
                if i == 0: # 최종 목표
                    goal['title'], goal['content'], goal['require'] = setFinalObjective(town, town_detail, genre, background)
                    f_title = goal['title']
                    f_content = goal['content']
                    goal['chapter'] = 5
                else:
                    goal['chapter'] = i
                    goal['req_type'], goal['title'], goal['content'], goal['require'], goal['etc'] = setChapterObjective(i-1, "", f_title, f_content, town, town_detail, genre, background)
                
                goals.append(goal)
                
        # chapter가 2 ~ 4일때는 해당 챕터 목표 생성
        else:
            # 이전 플레이 요약본 필요
            gpts = Gpt.objects.filter(script=pk).filter(chapter=chapter-1)
            prev_summ = ""
            for gpt in gpts:
                prev_summ += gpt['query'] + "\n"
            goal['chapter'] = chapter
            goal['type'], goal['title'], goal['content'], goal['require'], goal['etc'] = setChapterObjective(chapter-1, prev_summ, f_title, f_content, town, town_detail, genre, background)
            goals.append(goal)
        
        # 목표 정보 저장
        serializer = self.serializer_class(data=goals, many=True)
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
    
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def get(self, request, pk, chapter):
        auth_token = get_token_key(request=request)
        user_id = get_user_id_from_token(token_key=auth_token)
        user = get_object_or_404(User, pk=user_id)
        
        if CheckAuth(user=user, model_name=Script, pk=pk):
            return Response({
                'message' : '목표 상세 조회 권한이 없습니다.'
            }, status=HTTP_400_BAD_REQUEST)
        
        if(chapter == 0):
            goals = Goal.objects.filter(script=pk)
        else:
            goals = Goal.objects.filter(script=pk).filter(chapter=chapter)
            
        serializer = self.serializer_class(goals, many=True)
        
        return Response({
            'message' : '목표 상세 조회 성공',
            'data' : serializer.data
        }, status=HTTP_200_OK)
    
    def patch(self, request, pk, chapter):
        if CheckAuth(request, Script, pk):
            return Response({
                'message' : '목표 정보 수정 권한이 없습니다.'
            }, status=HTTP_400_BAD_REQUEST)
        
        goal = Goal.objects.filter(script=pk).filter(chapter=chapter)
        serializer = self.serializer_class(data=request.data, instance=goal, partial=True)
        
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
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
from .views import *
from gpt.npc_function import *

# npc 생성 (pk : script_id)
class NpcView(views.APIView):
    serilalizer_class = NpcSerializer
    
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def post(self, request, pk):
        auth_token = get_token_key(request=request)
        user_id = get_user_id_from_token(token_key=auth_token)
        user = get_object_or_404(User, pk=user_id)
        
        if CheckAuth(user=user, model_name=Character, pk=pk):
            return Response({
                'message' : 'npc 생성 권한이 없습니다.'
            }, status=HTTP_400_BAD_REQUEST)
        
        # npc 생성에 필요한 정보
        script = get_object_or_404(Script, pk=pk)
        background = script.background
        genre = script.genre
        town = script.town
        
        npcs = []
        for i in range(0, 2):
            npc = {'name': '', 'role': '', 'info': ''}
            if i == 0:
                # script 정보 토대로 npc 생성 (조력자)
                npc['role'] = "prota"
                npc['name'] = getProtaNPCName(background=background, genre=genre)
                npc['info'] = getProtaNPCInfo(town=town, PNPC_name=npc['name'])
            else:
                # script 정보 토대로 npc 생성 (대력자)
                npc['role'] = "anta"
                npc['name'] = getAntaNPCName(background=background, genre=genre)
                npc['info'] = getAntaNPCInfo(town=town, ANPC_name=npc['name'])

            npcs.append(npc)
        
        print(npcs)
        
        # NPC 저장
        serializer = self.serilalizer_class(data=npcs, many=True)
        
        if serializer.is_valid(raise_exception=True): 
            serializer.save(script=script)
            return Response({
                'message' : 'NPC(조력자 / 적대자) 생성 성공',
                'data' : serializer.data
            }, status=HTTP_200_OK)
        else:
            return Response({
                'message' : 'NPC(조력자 / 적대자) 생성 실패',
                'data' : serializer.errors
            }, status=HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        npcs = Npc.objects.filter(script=pk)
        serializer = self.serilalizer_class(npcs, many=True)
        
        return Response({
            'message' : 'NPC 조회 성공',
            'data' : serializer.data
        }, status=HTTP_200_OK)
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication

from .models import *
from .serializers import *
from account.views import *

# 캐릭터 생성 뷰
class CharacterView(views.APIView):
    serilalizer_class = CharacterSerializer
    
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def post(self, request):
        serializer = self.serilalizer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            auth_token = get_token_key(request=request)
            user_id = get_user_id_from_token(token_key=auth_token)
            
            user = get_object_or_404(User, pk=user_id)
            serializer.save(user=user)
            return Response({
                'message' : '캐릭터 생성 성공',
                'data' : serializer.data
            }, status=HTTP_200_OK)
        else:
            return Response({
                'message' : '캐릭터 생성 실패',
                'data' : serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
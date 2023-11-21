from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.status import *
from rest_framework.response import Response

from .models import *
from .serializers import *

# GPT 대화내용 (pk : script_id) - 저장 / 조회
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
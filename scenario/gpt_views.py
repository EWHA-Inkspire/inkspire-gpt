from .views import *
from .models import Script, Gpt
from .serializers import GptSerializer
from gpt.gpt_function import summary

# GPT 대화내용 (pk : script_id) - 저장 / 조회
class GptView(views.APIView):
    serializer_class = GptSerializer
    
    def post(self, request, pk):
        script = get_object_or_404(Script, pk=pk)
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            summ = summary(response=request.data.get('content'))
            serializer.validated_data['summary'] = summ
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
        serializer = self.serializer_class(gpts, many=True)
        
        return Response({
            'message' : 'GPT 조회 성공',
            'data' : serializer.data
        }, status=HTTP_200_OK)
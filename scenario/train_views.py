from .views import *
from .serializers import TrainSerializer

class TrainView(views.APIView):
    serializer_class = TrainSerializer
    
    def get(self, request, pk):
        trains = Train.objects.filter(script=pk)

        serializer = self.serializer_class(trains, many=True)
        
        return Response({
            'message' : 'Train data 조회 성공',
            'data' : serializer.data
        }, status=HTTP_200_OK)
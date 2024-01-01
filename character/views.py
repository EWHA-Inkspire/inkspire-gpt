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

# 인벤토리 도구 등록, 삭제
# pk : character_id
class InventoryView(views.APIView):
    serializer_class = InventorySerializer
    
    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            character = get_object_or_404(Character, pk=pk)
            serializer.save(character=character)
            return Response({
                'message' : '도구 등록 성공',
                'data' : serializer.data
            }, status=HTTP_200_OK)
        else:
            return Response({
                'message' : '도구 등록 실패',
                'data' : serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, item_pk):
        item = get_object_or_404(Inventory, pk=item_pk)
        item.delete()
        
        return Response({
            'message' : '도구 삭제 성공',
        }, status=HTTP_200_OK)
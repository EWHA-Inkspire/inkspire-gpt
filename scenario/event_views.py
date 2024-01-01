from .views import *
from .serializers import EventSerializer
from gpt.event_function import *

# 이벤트 생성 뷰 (pk : script_id, chapter : 1 ~ 5)
# script/<int:pk>/<int:chapter>/event
class EventView(views.APIView):
    serializer_class = EventSerializer
    
    def get(self, request, pk, chapter):
        event = Goal.objects.filter(script=pk).filter(chapter=chapter)
            
        serializer = self.serializer_class(event, many=True)
        
        return Response({
            'message' : '목표 상세 조회 성공',
            'data' : serializer.data
        }, status=HTTP_200_OK)
        
    def patch(self, request, pk, chapter):
        # 이벤트 생성에 필요한 정보 (background, town_detail, obj, obj_req)
        script = get_object_or_404(Script, pk=pk)
        background = script.background
        town_detail = script.town_detail
        goal = get_object_or_404(Goal, script=pk, chapter=chapter)
        print(goal)
        obj = goal.content
        obj_req = goal.require
        
        # 이벤트 정보 생성
        event_require, event_content, event_success, event_fail = setDiceEvent(background, town_detail, obj, obj_req)
        
        result, created = Goal.objects.update_or_create(
            script = pk,
            chapter = chapter,
            defaults={"event_req": event_require, "event_content" : event_content, "success" : event_success, "fail" : event_fail}
        )
        
        serializer = self.serializer_class(result)
        
        return Response({
            'message' : '이벤트 생성 성공',
            'data' : serializer.data
        }, status=HTTP_200_OK)
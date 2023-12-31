from .views import *
import gpt.const as c
from gpt.gpt_function import callGPT, summary
from .serializers import GptSerializer, TrainSerializer
from gpt.play_function import setIntroQuery, setPlayQuery

# 게임 intro 플레이 뷰
# post: intro 스크립트 생성
class GameStartView(views.APIView):
    gpt_serializer_class = GptSerializer
    train_serializer_class = TrainSerializer
    
    def post(self, request):
        # intro 스크립트 생성
        query = setIntroQuery(request)
        system_intro = c.SYSTEM_INTRO
        
        messages = [
            {"role": "system", "content": system_intro},
            {"role": "user", "content": query}
        ]
        
        # callGPT 돌리기
        response = callGPT(messages=messages, stream=True)
        messages.append({
            "role" : "assistant",
            "content" : response
        })
        
        summ = summary(response=response)
        
        gpt_data = {'role' : "assistant", 'content' : response, 'summary': summ, 'chapter': 1}
        gpt_serializer = self.gpt_serializer_class(data=gpt_data)
        train_serializer = self.train_serializer_class(data=messages, many=True)
        
        # response 저장
        if gpt_serializer.is_valid(raise_exception=True) and train_serializer.is_valid(raise_exception=True):
            script = get_object_or_404(Script, pk=request.data.get('script_id'))
            gpt_serializer.save(script=script)
            train_serializer.save(script=script)
            return Response({
                'message' : 'GPT 쿼리 저장 성공',
                'data' : gpt_serializer.data
            }, status=HTTP_200_OK)
        else:
            return Response({
                'message' : 'GPT 쿼리 저장 실패',
                'data' : gpt_serializer.errors
            }, status=HTTP_400_BAD_REQUEST)

# 게임 play 뷰
class GamePlayVew(views.APIView):
    gpt_serializer_class = GptSerializer
    train_serializer_class = TrainSerializer
    
    def post(self, request, pk):
        system_play = c.SYSTEM_PLAY
        messages = [{"role": "system", "content": system_play}]
        
        # 이전 채팅 정보 요약
        chat_history = request.data.get('history')
        for history in chat_history:
            print(history)
            message = {"role": "", "content": ""}
            message['role'] = history['role']
            message['content'] = history['summary']
            messages.append(message)
        
        # user의 선택 => 요약 없이 그대로 저장
        content = request.data.get('query')
        # npc, 목표, plot 정보 추가
        train_content = setPlayQuery(request) + "사용자 입력값: #" + content + "#"
        chapter = request.data.get('chapter')
        gpts = [{"role" : "user", "content" : content, "summary": content, "chapter" : chapter}]
        
        # GPT 호출
        messages.append({"role": "user", "content": train_content})
        response = callGPT(messages=messages, stream=True)
        
        summ = summary(response=response)
        gpts.append({"role" : "assistant", "content" : response, "summary": summ, "chapter" : chapter})
        train_msg = [messages[0], {"role" : "user", "content" : train_content}, {"role" : "assistant", "content" : response}]
        
        gpt_serializer = self.gpt_serializer_class(data=gpts, many=True)
        train_serializer = self.train_serializer_class(data=train_msg, many=True)
        
        if gpt_serializer.is_valid(raise_exception=True) and train_serializer.is_valid(raise_exception=True):
            script = get_object_or_404(Script, pk=pk)
            gpt_serializer.save(script=script)
            train_serializer.save(script=script)
            return Response({
                'message' : '플레이어 입력 저장 성공',
                'data' : gpt_serializer.data
            }, status=HTTP_200_OK)
        else:
            return Response({
                'message' : '플레이어 입력 저장 실패',
                'data' : gpt_serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
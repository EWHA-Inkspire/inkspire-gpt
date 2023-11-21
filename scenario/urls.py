from django.urls import path
from .script_views import *
from .goal_views import *
from .gpt_views import *
from .npc_views import *

urlpatterns = [
    path('<int:pk>/script', ScriptView.as_view()),
    path('script/<int:pk>', ScriptListView.as_view()),
    path('script/<int:pk>/<int:chapter>/goal', GoalListView.as_view()),
    path('script/<int:pk>/chat', GptView.as_view()),
    path('script/<int:pk>/npc', NpcView.as_view()),
]
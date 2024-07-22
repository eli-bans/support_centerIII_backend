from django.urls import path
from .views import QuestionListCreateView, AnswerListCreateView, CommentListCreateView, VoteListCreateView

urlpatterns = [
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('answers/', AnswerListCreateView.as_view(), name='answer-list-create'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('votes/', VoteListCreateView.as_view(), name='vote-list-create'),
]

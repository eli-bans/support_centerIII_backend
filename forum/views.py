from rest_framework import generics, status
from .models import Question, Answer, Comment, Vote
from .serializers import QuestionSerializer, AnswerSerializer, CommentSerializer, VoteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class AnswerListCreateView(generics.ListCreateAPIView):
#     queryset = Answer.objects.all()
#     serializer_class = AnswerSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        print("Request data:", request.data)  # Debug print
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        question_id = serializer.validated_data['question'].id
        content = serializer.validated_data['content']
        
        try:
            question = Question.objects.get(id=question_id)
            answer = Answer.objects.create(
                question=question,
                user=request.user,
                content=content
            )
            return Response(AnswerSerializer(answer).data, status=status.HTTP_201_CREATED)
        except Question.DoesNotExist:
            return Response({"error": "Question does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Error:", str(e))  # Debug print
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# from rest_framework import generics, status
# from rest_framework.response import Response
# from .models import Comment, Answer
# from .serializers import CommentSerializer

# class CommentListCreateView(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

#     def create(self, request, *args, **kwargs):
#         print("Request data:", request.data)  # Debug print
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         answer_id = serializer.validated_data['answer'].id
#         content = serializer.validated_data['content']
        
#         try:
#             answer = Answer.objects.get(id=answer_id)
#             comment = Comment.objects.create(
#                 answer=answer,
#                 user=request.user,
#                 content=content
#             )
#             return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
#         except Answer.DoesNotExist:
#             return Response({"error": "Answer does not exist"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             print("Error:", str(e))  # Debug print
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         print(f"Number of comments: {queryset.count()}")  # Debug print
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

# class VoteListCreateView(generics.ListCreateAPIView):
#     queryset = Vote.objects.all()
#     serializer_class = VoteSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

class VoteListCreateView(generics.ListCreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


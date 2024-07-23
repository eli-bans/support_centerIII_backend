from rest_framework import serializers
from .models import Question, Answer, Comment, Vote

class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Question
        fields = ['id', 'user', 'title', 'content', 'timestamp']

# class AnswerSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.email')
#     question = serializers.ReadOnlyField(source='question.id')

#     class Meta:
#         model = Answer
#         fields = ['id', 'question', 'user', 'content', 'timestamp']


class AnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(),
        source='question',
        write_only=True
    )
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Answer
        fields = ['id', 'question_id', 'user', 'content', 'timestamp']

    def create(self, validated_data):
        print("Validated data in create:", validated_data)  # Debug print
        return Answer.objects.create(**validated_data)

# class CommentSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.email')
#     answer = serializers.ReadOnlyField(source='answer.id')

#     class Meta:
#         model = Comment
#         fields = ['id', 'answer', 'user', 'content', 'timestamp']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    answer_id = serializers.PrimaryKeyRelatedField(
        queryset=Answer.objects.all(),
        source='answer',
        write_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'answer_id', 'user', 'content', 'timestamp']

# class VoteSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.email')
#     answer = serializers.ReadOnlyField(source='answer.id')

#     class Meta:
#         model = Vote
#         fields = ['id', 'answer', 'user', 'vote_type']


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    answer_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'answer', 'answer_id', 'user', 'vote_type']
        read_only_fields = ['answer']

    def create(self, validated_data):
        answer_id = validated_data.pop('answer_id')
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            raise serializers.ValidationError("Answer not found.")
        validated_data['answer'] = answer
        return super().create(validated_data)


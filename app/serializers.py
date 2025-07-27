from rest_framework import serializers, status
from app.models import Conversation, Dialogue

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at']
        read_only_fields = ['created_at']

class DialogueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialogue
        fields = ['content', 'reply', 'created_at']
        read_only_fields = ['created_at']

class ConversationCreateSerializer(serializers.Serializer):
    content = serializers.CharField(required=True)
    title = serializers.CharField(required=False)
    conversation_id = serializers.CharField(required=False)
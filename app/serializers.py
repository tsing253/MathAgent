from rest_framework import serializers
from app.models import User, Group, Conversation, Dialogue

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'role']
        read_only_fields = ['id']

class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'members', 'created_at']
        read_only_fields = ['id', 'created_at']

class DialogueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialogue
        fields = ['id', 'content', 'reply', 'timestamp']
        read_only_fields = ['id', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    dialogues = DialogueSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'user', 'dialogues', 'created_at']
        read_only_fields = ['id', 'created_at']

class ConversationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['title']

class DialogueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dialogue
        fields = ['content', 'reply']
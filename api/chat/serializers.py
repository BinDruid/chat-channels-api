from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, Conversation
from api.users.serializers import UserSerializer


User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):
    chatter = serializers.SerializerMethodField()
    conversation = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "conversation",
            "chatter",
            "content",
            "timestamp",
            "is_seen",
        )

    def get_conversation(self, obj):
        return str(obj.conversation.id)

    def get_chatter(self, obj):
        return UserSerializer(obj.chatter).data


class ConversationListSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["id", "owner", "name", "last_message"]

    def get_last_message(self, obj):
        return MessageSerializer(obj.last_message()).data


class ConversationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        exclude = ("owner",)

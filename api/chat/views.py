from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Conversation
from .serializers import (
    ConversationDetailSerializer,
    ConversationCreateSerializer,
    ConversationListSerializer,
)


class ActionMixin:
    def get_serializer_class(self):
        return self.serializer_per_action

    def get_queryset(self):
        return self.queryset_per_action


class ChatConversationView(ActionMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]

    lookup_field = "pk"

    @property
    def serializer_per_action(self):
        serializer_classes = {
            "list": ConversationListSerializer,
            "retrieve": ConversationDetailSerializer,
            "create": ConversationCreateSerializer,
        }
        return serializer_classes[self.action]

    @property
    def queryset_per_action(self):
        queryset_classes = {
            "list": Conversation.objects.filter(members__user=self.request.user),
            "retrieve": Conversation.objects.filter(owner=self.request.user),
            "create": Conversation.objects.all(),
        }
        return queryset_classes[self.action]

    def create(self, request, *args, **kwargs):
        """
        Create a session with user as the owner and add him as a memeber of it.
        """
        response = super().create(request, *args, **kwargs)
        new_chat_member = Conversation()
        new_chat_member.chat_session_id = response.data["id"]
        new_chat_member.user = self.request.user
        new_chat_member.save()
        response.data["message"] = "You have joined new chat session!"
        return response

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ApiRootView(APIView):
    """
    Lists currently avaiable endpoints.
    """

    def get(self, request, format=None):
        return Response(
            {
                "chat_sessions": reverse(
                    "chat_sessions", request=request, format=format
                ),
                "chatters": reverse("chatters", request=request, format=format),
            }
        )

from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Conversation
from .serializers import ConversationUpdateSerializer, ConversationListSerializer


User = get_user_model()


class ActionMixin:
    def get_serializer_class(self):
        return self.serializer_per_action

    def get_queryset(self):
        return self.queryset_per_action


class ConversationView(ActionMixin, ModelViewSet):
    permission_classes = [IsAuthenticated]

    lookup_field = "pk"

    @property
    def serializer_per_action(self):
        serializer_classes = {
            "list": ConversationListSerializer,
            "partial_update": ConversationUpdateSerializer,
        }
        return serializer_classes[self.action]

    @property
    def queryset_per_action(self):
        queryset_classes = {
            "list": Conversation.objects.filter(chatters=self.request.user),
            "partial_update": Conversation.objects.all(),
        }
        return queryset_classes[self.action]

    def perform_update(self, serializer):
        action = self.request.data["action"]
        instance = self.get_object()
        user = self.request.user
        perform_action_method = getattr(instance, action, None)
        if perform_action_method is None:
            raise ValueError(f"Invalid action: It should be either join or leave!")
        perform_action_method(user)
        instance.save()

    def list(self, request, *args, **kwargs):
        """
        Returns pivot and filter parameters in response.
        """
        response = super().list(request, args, kwargs)
        return response


class ApiRootView(APIView):
    """
    Lists currently available endpoints.
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

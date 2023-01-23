from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response


# from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
# from rest_framework.viewsets import GenericViewSet

# from .models import Conversation, Message
# from .serializers import MessageSerializer, ConversationSerializer


# class ConversationViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
#     serializer_class = ConversationSerializer
#     queryset = Conversation.objects.all()


# class MessageViewSet(ListModelMixin, GenericViewSet):
#     serializer_class = MessageSerializer
#     queryset = Message.objects.all()


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

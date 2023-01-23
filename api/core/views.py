from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response


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

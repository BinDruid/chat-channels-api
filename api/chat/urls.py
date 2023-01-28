from django.urls import path
from .views import ApiRootView, ConversationView

urlpatterns = [
    path("", ApiRootView.as_view(), name="home"),
    path(
        "conversations/",
        (ConversationView.as_view({"get": "list"})),
        name="conversation",
    ),
    path(
        "conversations/<uuid:pk>/members/",
        (ConversationView.as_view({"patch": "partial_update"})),
        name="conversation_update",
    ),
]

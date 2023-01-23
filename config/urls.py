from django.contrib import admin
from django.urls import path, include
from api.users.views import AuthTokenView


urlpatterns = [
    path("master/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += [
    # path("", include("apps.core.urls")),
    path("v1/auth/", AuthTokenView.as_view()),
    path("v1/chats/", include("api.chat.urls")),
]
